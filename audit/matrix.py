#!/usr/bin/env python3
"""Traceability matrix: the claims of one source against the skill files, judged by Jev.

    python3 audit/matrix.py --source audit/runs/sources/<id>.txt --claims audit/sources/<id>.claims.json \
        --skills skills --out audit/runs/<run>/<id> [--no-jev] [--only C3,C6]

Claims file: a JSON list of {"id", "claim", "quote", "status", "refs": [{"file", "anchor"}], "reason"}.
  quote   must appear verbatim in the source text (whitespace runs collapsed).
  status  covered | partial | gap | infra | rejected. gap and partial name the missing line in "reason".
  refs    the skill lines that cover the claim; "anchor" is a phrase unique to one line of "file".
Writes <out>.matrix.md, <out>.jev.json and <out>.summary.json. Exit 1 when a quote or an anchor does not resolve."""
import argparse, json, os, pathlib, re, subprocess, sys

JUDGE = os.environ.get("JUDGE_PY", os.path.expanduser("~/.claude/plugins/marketplaces/sensibility/skills/judge/scripts/judge.py"))
QUESTIONS = {
    "covered": {"type": "noul", "instructions": "Does `skill_excerpt` instruct the agent to do what `claim` describes?",
                "criteria": {"true": "The excerpt tells the agent to do the thing the claim describes, or forbids what the claim warns against.",
                             "false": "The excerpt is about something else, covers only a part of the claim, or states a principle without telling the agent to act."}},
    "doable": {"type": "noul", "instructions": "Can a coding agent with a shell, file access and read-only access to logs, metrics and production hosts do what `claim` describes on its own, without a human?",
               "criteria": {"true": "The agent can do it alone with those tools.", "false": "It needs a human decision, access only a human has, or infrastructure that must be built first."}},
    "specificity": {"type": "score", "instructions": "How specific is `skill_excerpt` as an instruction for the part of `claim` it covers?",
                    "criteria": ["Nothing in the excerpt tells the agent to act.", "A principle only: it says what matters but not what to do.",
                                 "An action with no trigger: it says what to do but not when.", "An action with a trigger but no check: it says what and when, but not how the agent knows it is done.",
                                 "An action with a trigger and a done condition the agent can check."]}}

def norm(s): return re.sub(r"\s+", " ", s).strip()

def jev(state):
    p = subprocess.run([sys.executable, JUDGE, json.dumps(QUESTIONS), "--state", json.dumps(state, ensure_ascii=False)], capture_output=True, text=True)
    try: return json.loads(p.stdout.strip().splitlines()[-1])["answers"]
    except Exception: return {"error": (p.stdout + p.stderr)[-300:]}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--source", required=True); ap.add_argument("--claims", required=True)
    ap.add_argument("--skills", required=True); ap.add_argument("--out", required=True); ap.add_argument("--no-jev", action="store_true"); ap.add_argument("--only", default="")
    a = ap.parse_args()
    source = norm(pathlib.Path(a.source).read_text()); skills = pathlib.Path(a.skills)
    claims = json.loads(pathlib.Path(a.claims).read_text()); only = set(a.only.split(",")) if a.only else None
    out = pathlib.Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    cache = {}
    def lines(f):
        if f not in cache: cache[f] = (skills / f).read_text().splitlines()
        return cache[f]
    rows, verdicts, misses = [], {}, {"quote": [], "anchor": []}
    for c in claims:
        if only and c["id"] not in only: continue
        if norm(c["quote"]) not in source: misses["quote"].append(c["id"])
        cells = []
        for r in c.get("refs", []):
            hits = [n for n, l in enumerate(lines(r["file"]), 1) if r["anchor"] in l]
            if len(hits) != 1: misses["anchor"].append(f"{c['id']} {r['file']} {r['anchor'][:40]!r} hits={len(hits)}" + (" (added " + r["added"] + ")" if r.get("added") else "")); continue
            cells.append(f"{r['file']}:{hits[0]}: {lines(r['file'])[hits[0]-1].strip()}")
        excerpt = "\n".join(cells) or "(no skill line covers this claim)"
        ans = {} if a.no_jev else jev({"claim": c["claim"] + " Quote from the source: " + c["quote"], "skill_excerpt": excerpt})
        verdicts[c["id"]] = {"excerpt": excerpt, "answers": ans}
        def g(k):
            v = ans.get(k)
            if not isinstance(v, dict): return ""
            return f"{v['score'] + 1:.1f}" if k == "specificity" else f"{v['noul']:.2f}"
        refs = ", ".join(x.split(": ", 1)[0] for x in cells) or "-"
        c["status_now"] = c["status"] if c["status"] in ("infra", "rejected") else ("no line" if not cells else "has lines")
        rows.append((c, refs, g("covered"), g("doable"), g("specificity")))
    def status_of(c): return c["status"]
    recheck = []
    for c, refs, cov, doable, spec in rows:
        if cov == "": continue
        if c["status"] == "covered" and float(cov) < 0.5: recheck.append(f"{c['id']}: marked covered, Jev {cov}")
        if c["status"] in ("gap", "partial") and float(cov) >= 0.5: recheck.append(f"{c['id']}: marked {c['status']}, Jev {cov}")
    counts = {}
    for c, *_ in rows: counts[c["status"]] = counts.get(c["status"], 0) + 1
    no_line = [c["id"] for c, *_ in rows if c["status_now"] == "no line"]
    weak = [f"{c['id']} ({c['status']}) Jev {cov}" for c, refs, cov, *_ in rows if cov and float(cov) < 0.5 and c["status"] not in ("infra", "rejected")]
    md = ["| # | Claim | Status | Skill lines | Jev covered | doable | specificity 1 to 5 |", "|---|---|---|---|---|---|---|"]
    md += [f"| {c['id']} | {c['claim']} | {c['status']}{(' (' + c['reason'] + ')') if c.get('reason') and c['status'] != 'covered' else ''} | {refs} | {cov} | {doable} | {spec} |" for c, refs, cov, doable, spec in rows]
    md += ["", "## Quotes", ""] + [f"- **{c['id']}** “{c['quote']}”" for c, *_ in rows]
    pathlib.Path(str(out) + ".matrix.md").write_text("\n".join(md) + "\n")
    pathlib.Path(str(out) + ".jev.json").write_text(json.dumps(verdicts, indent=1, ensure_ascii=False))
    summary = {"source": a.source, "claims": len(rows), "counts": counts, "recheck": recheck, "quote_misses": misses["quote"], "anchor_misses": misses["anchor"],
               "recorded_gaps": [c["id"] for c, *_ in rows if c["status"] in ("gap", "partial")], "no_line_now": no_line, "jev_below_half": weak}
    pathlib.Path(str(out) + ".summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary, indent=1))
    hard = [m for m in misses["anchor"] if "(added" not in m]
    sys.exit(1 if misses["quote"] or hard else 0)

if __name__ == "__main__": main()
