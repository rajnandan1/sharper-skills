#!/usr/bin/env python3
"""Assemble one release report from a run directory.

    python3 audit/report.py audit/runs/<run> > audit/runs/<run>/report.md

Reads every *.summary.json, *.matrix.md, *.counts.json, *.flagged.md and *.grades.json in the directory."""
import json, pathlib, sys
run = pathlib.Path(sys.argv[1])
out = [f"# sharper-skills audit, run {run.name}", ""]
sums = sorted(run.glob("*.summary.json"))
if sums:
    out += ["## Sources against skills", "", "| Source | Claims | Covered | Partial | Gap | Infra | Rejected | Re-check |", "|---|---|---|---|---|---|---|---|"]
    for s in sums:
        d = json.loads(s.read_text()); c = d["counts"]
        out.append(f"| {s.name.replace('.summary.json','')} | {d['claims']} | {c.get('covered',0)} | {c.get('partial',0)} | {c.get('gap',0)} | {c.get('infra',0)} | {c.get('rejected',0)} | {len(d['recheck'])} |")
    for s in sums:
        d = json.loads(s.read_text())
        if d["recheck"]: out += ["", f"Re-check list for {s.name.replace('.summary.json','')}: " + "; ".join(d["recheck"])]
        if d["quote_misses"] or d["anchor_misses"]: out += ["", f"Unresolved in {s.name}: quotes {d['quote_misses']}, anchors {d['anchor_misses']}"]
for c in sorted(run.glob("*.counts.json")):
    out += ["", f"## Transcripts: {c.name.replace('.counts.json','')}", "", "```json", c.read_text().strip(), "```"]
    f = c.with_name(c.name.replace(".counts.json", ".flagged.md"))
    if f.exists(): out += ["", f.read_text().split("\n", 2)[-1]]
for g in sorted(run.glob("*.grades.json")):
    out += ["", f"## Behavioural run: {g.name.replace('.grades.json','')}", "", "```json", g.read_text().strip(), "```"]
for m in sorted(run.glob("*.matrix.md")):
    out += ["", f"## Matrix: {m.name.replace('.matrix.md','')}", "", m.read_text()]
print("\n".join(out))
