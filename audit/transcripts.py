#!/usr/bin/env python3
"""What the human did after a skill ran, from the Claude Code transcripts on this machine.

    python3 audit/transcripts.py --mode debug --skills debugging-by-constraints signal-first-plan --out audit/runs/<run>/debug
    python3 audit/transcripts.py --mode lens  --skills higher deeper wider --out audit/runs/<run>/lens

debug mode: every human-typed message after the skill fired, up to the next unrelated slash command, classified with Jev
into debug-retro's kinds (control, fact, constraint, proxy, method, decision) plus question and other. A pasted image
counts as proxy. lens mode: the first human reply after the lens handed its rewrite back, classified as ran_as_is,
edited, dropped or other. Writes <out>.jsonl, <out>.counts.json and <out>.flagged.md."""
import argparse, collections, json, os, pathlib, re, subprocess, sys

JUDGE = os.environ.get("JUDGE_PY", os.path.expanduser("~/.claude/plugins/marketplaces/sensibility/skills/judge/scripts/judge.py"))
OURS = {"debugging-by-constraints", "signal-first-plan", "debug-retro", "higher", "deeper", "wider"}
NOISE = ("Base directory for this skill", "Tool loaded", "<task-notification>", "<local-command", "[Request interrupted", "Called the ",
         "<command-message>", "<system-reminder", "Another Claude session", "[Cross-session", "This session is being continued", "(Re-invocation",
         "Your response above was stopped")
KINDS = {"control": "Gives the agent a comparison case to check against, or asks it to set one up.",
         "fact": "Supplies data, or points at a file, path, value or record the agent had not looked at.",
         "constraint": "Pushes back on the agent's conclusion or plan with a fact that contradicts it.",
         "proxy": "Reports the result of a command the human ran, pastes output or a screenshot, or quotes a dashboard number the agent could have read itself.",
         "method": "Tells the agent how to work: reproduce it, cite, split the hypothesis, go a layer down, try on your own, widen the scope, do it in one PR.",
         "decision": "Approves, picks an option, says merge, deploy, post, roll back, escalate, or sets scope; includes short yes or ok replies and numbered yes lists.",
         "question": "Asks the agent to explain or recall something, with no instruction.",
         "other": "A new unrelated request, or none of the above."}
LENS_KINDS = {"ran_as_is": "Says go, run it, yes, or pastes the rewrite back unchanged, so the rewrite runs as handed back.",
              "edited": "Asks for a change to the rewrite, or pastes a changed version of it, before it runs.",
              "dropped": "Starts a different request and never runs the rewrite.",
              "other": "A question about the rewrite, or none of the above."}

def flat(s): return re.sub(r"\s+", " ", s or "")

def text_of(msg):
    c = msg.get("content")
    if isinstance(c, str): return c
    return "\n".join(b["text"] for b in (c or []) if isinstance(b, dict) and b.get("type") == "text")

def human_text(o, msg):
    if o.get("isMeta"): return None
    c = msg.get("content")
    if isinstance(c, list) and c and all(isinstance(b, dict) and b.get("type") == "tool_result" for b in c): return None
    t = re.sub(r"<system-reminder>.*?</system-reminder>", "", text_of(msg), flags=re.S).strip()
    if not t or any(t.startswith(n) for n in NOISE): return None
    return t

def judge(questions, state):
    p = subprocess.run([sys.executable, JUDGE, json.dumps(questions), "--state", json.dumps(state, ensure_ascii=False)], capture_output=True, text=True)
    try: return json.loads(p.stdout.strip().splitlines()[-1])["answers"]
    except Exception: return {"error": (p.stdout + p.stderr)[-300:]}

def sessions(projects, skills):
    for f in pathlib.Path(projects).rglob("*.jsonl"):
        try: lines = f.read_text(errors="replace").splitlines()
        except Exception: continue
        objs = []
        for l in lines:
            if not l.startswith("{"): continue
            try: objs.append(json.loads(l))
            except json.JSONDecodeError: continue
        yield f, objs

def fired_at(objs, skills):
    for i, o in enumerate(objs):
        msg = o.get("message") or {}; role = msg.get("role")
        if role == "user":
            m = re.search(r"<command-name>/(?:sharper-skills:)?([a-z-]+)<", text_of(msg))
            if m and m.group(1) in skills: return i, m.group(1)
        if role == "assistant":
            for b in (msg.get("content") or []):
                if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "Skill" and (b.get("input") or {}).get("skill", "").split(":")[-1] in skills:
                    return i, b["input"]["skill"].split(":")[-1]
    return None, None

def debug_rows(projects, skills):
    rows, n_sessions = [], 0
    for f, objs in sessions(projects, skills):
        start, which = fired_at(objs, skills)
        if start is None: continue
        n_sessions += 1
        for o in objs[start + 1:]:
            msg = o.get("message") or {}
            if msg.get("role") != "user": continue
            raw = text_of(msg)
            m = re.search(r"<command-name>/(?:sharper-skills:)?([a-z-]+)<", raw)
            if m and m.group(1) not in OURS: break
            if m: continue
            t = human_text(o, msg)
            if t is None: continue
            if t.startswith("[Image:"): rows.append({"session": f.stem[:8], "skill": which, "ts": o.get("timestamp", ""), "text": "(pasted image)", "kind": "proxy", "conf": 1.0}); continue
            rows.append({"session": f.stem[:8], "skill": which, "ts": o.get("timestamp", ""), "text": t[:400]})
    seen, dedup = set(), []
    for r in rows:
        k = (r["session"], r["text"][:200])
        if k not in seen: seen.add(k); dedup.append(r)
    return dedup, n_sessions

def lens_rows(projects, skills):
    rows = []
    for f, objs in sessions(projects, skills):
        start, which = fired_at(objs, skills)
        if start is None: continue
        rewrite, reply = None, None
        for o in objs[start + 1:]:
            msg = o.get("message") or {}
            if msg.get("role") == "assistant" and rewrite is None:
                m = re.search(r"```(?:\w+)?\n(.*?)```", text_of(msg), re.S)
                if m: rewrite = m.group(1).strip()
            elif msg.get("role") == "user" and rewrite is not None:
                t = human_text(o, msg)
                if t is None or t.startswith("[Image:"): continue
                reply = t[:600]; break
        rows.append({"session": f.stem[:8], "skill": which, "rewrite": (rewrite or "")[:600], "reply": reply, "kind": None if reply else "no_reply"})
    return rows

def classify(rows, kinds, key, with_rewrite=False):
    todo = [r for r in rows if r.get("kind") is None]
    for s in range(0, len(todo), 10):
        batch = todo[s:s + 10]
        state = {f"m{i}": ({"rewrite": r["rewrite"], "reply": r[key]} if with_rewrite else r[key]) for i, r in enumerate(batch, 1)}
        qs = {f"m{i}": {"type": "choice", "instructions": (f"The agent handed back the prompt `m{i}.rewrite`. What kind of reply is `m{i}.reply`?" if with_rewrite else f"In a session where a coding agent debugs or builds, which kind of human message is `m{i}`?"), "criteria": kinds} for i in range(1, len(batch) + 1)}
        ans = judge(qs, state)
        if "error" in ans: print("Jev error:", ans["error"], file=sys.stderr); return
        for i, r in enumerate(batch, 1):
            r["kind"] = ans[f"m{i}"]["choice"]; r["conf"] = round(ans[f"m{i}"].get("confidence", 0), 2)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--mode", choices=["debug", "lens"], required=True); ap.add_argument("--skills", nargs="+", required=True)
    ap.add_argument("--projects", default=os.path.expanduser("~/.claude/projects")); ap.add_argument("--out", required=True); ap.add_argument("--no-jev", action="store_true")
    a = ap.parse_args(); out = pathlib.Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    if a.mode == "debug":
        rows, n = debug_rows(a.projects, set(a.skills))
        if not a.no_jev: classify(rows, KINDS, "text")
        counts = collections.Counter(r.get("kind") or "unclassified" for r in rows)
        flagged = [r for r in rows if r.get("kind") in ("control", "fact", "constraint", "proxy", "method")]
        md = [f"# Human messages after {', '.join(a.skills)} fired", "", f"Sessions where a skill fired: {n}. Human-typed messages in the window: {len(rows)}. Sessions with messages: {len({r['session'] for r in rows})}.", "", "| Kind | Count |", "|---|---|"]
        md += [f"| {k} | {v} |" for k, v in counts.most_common()]
        md += ["", "## Messages that count as the agent's mistakes (control, fact, constraint, proxy, method)", ""]
        md += [f"- [{r['kind']} {r.get('conf', '')}] {r['session']} {r['skill']}: {flat(r['text'])[:220]}" for r in flagged]
        md += ["", "## Questions the human asked (a question often names data the agent should have shown)", ""]
        md += [f"- {r['session']} {r['skill']}: {flat(r['text'])[:220]}" for r in rows if r.get("kind") == "question"]
        summary = {"sessions_fired": n, "messages": len(rows), "counts": dict(counts), "flagged": len(flagged)}
    else:
        rows = lens_rows(a.projects, set(a.skills))
        if not a.no_jev: classify(rows, LENS_KINDS, "reply", with_rewrite=True)
        counts = {s: dict(collections.Counter(r.get("kind") or "unclassified" for r in rows if r["skill"] == s)) for s in a.skills}
        md = [f"# What the human did after {', '.join(a.skills)} handed back a rewrite", "", "| Lens | " + " | ".join(list(LENS_KINDS) + ["no_reply"]) + " |", "|---|" + "---|" * (len(LENS_KINDS) + 1)]
        md += [f"| {s} | " + " | ".join(str(counts[s].get(k, 0)) for k in list(LENS_KINDS) + ["no_reply"]) + " |" for s in a.skills]
        md += ["", "## Edited replies", ""] + [f"- {r['session']} {r['skill']}: {flat(r['reply'])[:300]}" for r in rows if r.get("kind") == "edited"]
        summary = {"sessions": len(rows), "counts": counts}
    pathlib.Path(str(out) + ".jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows))
    pathlib.Path(str(out) + ".counts.json").write_text(json.dumps(summary, indent=1))
    pathlib.Path(str(out) + ".flagged.md").write_text("\n".join(md) + "\n")
    print(json.dumps(summary, indent=1))

if __name__ == "__main__": main()
