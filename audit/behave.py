#!/usr/bin/env python3
"""Behavioural run: a fresh headless Claude follows the skill text of a given tree on a fixed case; Jev grades the trace.

    python3 audit/behave.py --family debugging --skills skills --out audit/runs/<run>/behave-after
    python3 audit/behave.py --family lenses    --skills skills --out audit/runs/<run>/behave-after [--tasks audit/cases/lens-tasks.json]

The skill text is inlined into the prompt, so the run tests the files in --skills, not the installed plugin.
Writes one .trace.md per run and <out>.grades.json with pass or fail per run."""
import argparse, json, os, pathlib, re, subprocess, sys

JUDGE = os.environ.get("JUDGE_PY", os.path.expanduser("~/.claude/plugins/marketplaces/sensibility/skills/judge/scripts/judge.py"))
HERE = pathlib.Path(__file__).resolve().parent
RULES = "Read nothing on disk, do not search the web, do not run shell commands, and do not spawn subagents. Where the skill says to dispatch a reviewer subagent, answer the REVIEWER items yourself in a labelled section at that point."

DEBUG_Q = {
    "control": {"type": "noul", "instructions": "Does `trace` name a control case, a working case the broken case is compared against?"},
    "matrix": {"type": "noul", "instructions": "Does `trace` contain a table with hypotheses as rows and facts as columns, with cells marked as fitting or contradicting?"},
    "strongest_signal": {"type": "noul", "instructions": "Does `trace` name the DNS lookup address count, about 5 against about 400, as the strongest signal, and call p99 latency a weak signal?"},
    "citations": {"type": "noul", "instructions": "In `trace`, does the explanation of the cause cite a numbered fact for each claim it makes?"},
    "cert_mistake": {"type": "noul", "instructions": "Does `trace` conclude that certificate reloading is the cause of the latency rise?"},
    "scale_kill": {"type": "noul", "instructions": "Does `trace` mark the hypothesis that the client sends requests to the wrong shard as contradicted only because pre-production showed no latency change?"}}
LENS_Q = {
    "deeper": {"same_deliverable": "Does `rewrite` ask for the same end result as `original`? Added measurements, checks, or a report of how the result was verified do not count as a new deliverable; new features, products, sections for other readers, or other audiences do.",
               "rawer_inputs": "Does `rewrite` ask to start from rawer material than `original` does, such as source data, logs or rows instead of a summary?",
               "named_instruments": "Does `rewrite` name specific methods, tools, commands or queries to use?",
               "outside_check": "Does `rewrite` ask for a check outside the model and the user that shows the result is right, such as a test, a measurement or a second tool?"},
    "higher": {"purpose_first": "Does the first sentence of `rewrite` state the purpose the task serves?",
               "outcome_one_up": "Does `rewrite` ask for the outcome that `original` serves, rather than for `original` itself?",
               "facts_kept": "Does `rewrite` keep every name, number and fact that appears in `original`?",
               "history_check": "Where past data or past runs exist for the task in `original`, does `rewrite` ask to show that the new way would have worked on them?"},
    "wider": {"same_deliverable": "Does `rewrite` ask for the same deliverable as `original`? Methods, checks, a red-team pass and a report of findings do not count as new deliverables; new features, products or audiences do.",
              "methods_not_characters": "Does `rewrite` describe methods to apply, as actions, rather than asking the model to play a persona?",
              "red_team": "Does `rewrite` include a step where someone tries to find the hole in the result before the user sees it?",
              "outside_field": "Does `rewrite` bring in a method from a field that `original` would not normally involve?"}}

def judge(questions, state):
    p = subprocess.run([sys.executable, JUDGE, json.dumps(questions), "--state", json.dumps(state, ensure_ascii=False)], capture_output=True, text=True)
    try: return json.loads(p.stdout.strip().splitlines()[-1])["answers"]
    except Exception: return {"error": (p.stdout + p.stderr)[-300:]}

def run_claude(prompt, timeout):
    p = subprocess.run(["claude", "-p", prompt, "--output-format", "text"], capture_output=True, text=True, timeout=timeout)
    return p.stdout if p.returncode == 0 else p.stdout + "\n[claude exit " + str(p.returncode) + "]\n" + p.stderr[-500:]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--family", choices=["debugging", "lenses"], required=True); ap.add_argument("--skills", required=True)
    ap.add_argument("--out", required=True); ap.add_argument("--tasks", default=str(HERE / "cases/lens-tasks.json")); ap.add_argument("--timeout", type=int, default=1500)
    ap.add_argument("--regrade", action="store_true", help="grade the saved traces again instead of running claude")
    a = ap.parse_args(); skills = pathlib.Path(a.skills); out = pathlib.Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    grades = {}
    if a.family == "debugging":
        d = skills / "debugging-by-constraints"
        skill_text = "\n\n".join(f"===== {n} =====\n" + (d / n).read_text() for n in ("SKILL.md", "LAYERS.md", "REVIEWER.md"))
        case = (HERE / "cases/latency-bug.md").read_text()
        prompt = f"You are a debugging agent. Follow the skill below exactly on the bug report that follows it. {RULES} You cannot gather new facts; where the skill needs one you do not have, write a ? cell and name the exact command that would gather it.\n\n{skill_text}\n\n===== BUG REPORT =====\n{case}"
        tp = pathlib.Path(str(out) + ".debugging.trace.md")
        trace = tp.read_text() if a.regrade else run_claude(prompt, a.timeout)
        tp.write_text(trace)
        ans = judge(DEBUG_Q, {"trace": trace[:60000]})
        g = {k: round(v["noul"], 2) for k, v in ans.items() if isinstance(v, dict) and "noul" in v}
        g["pass"] = all(g.get(k, 0) >= 0.5 for k in ("control", "matrix", "strongest_signal", "citations")) and g.get("cert_mistake", 1) < 0.5
        grades["debugging"] = g
    else:
        tasks = json.loads(pathlib.Path(a.tasks).read_text())
        for lens in ("higher", "deeper", "wider"):
            text = (skills / lens / "SKILL.md").read_text().split("---", 2)[-1]
            for t in tasks:
                prompt = text.replace("$ARGUMENTS", t["task"]) + "\n\nProduce the output now. Do not ask the user anything first."
                tp = pathlib.Path(str(out) + f".{lens}.{t['id']}.trace.md")
                trace = tp.read_text() if a.regrade else run_claude(prompt, a.timeout)
                tp.write_text(trace)
                m = re.search(r"```(?:\w+)?\n(.*?)```", trace, re.S); rewrite = m.group(1).strip() if m else trace
                qs = {k: {"type": "noul", "instructions": v} for k, v in LENS_Q[lens].items()}
                ans = judge(qs, {"original": t["task"], "rewrite": rewrite[:8000]})
                g = {k: round(v["noul"], 2) for k, v in ans.items() if isinstance(v, dict) and "noul" in v}
                g["pass"] = bool(g) and all(x >= 0.5 for x in g.values())
                grades[f"{lens}.{t['id']}"] = g
    pathlib.Path(str(out) + ".grades.json").write_text(json.dumps(grades, indent=1))
    print(json.dumps(grades, indent=1))

if __name__ == "__main__": main()
