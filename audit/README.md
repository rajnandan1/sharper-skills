# Audit

The skills in this repo come from written sources and run in real sessions. This folder checks both, so a release can say what the skills cover and what they still miss.

## What is here

- `sources/sources.json` lists each source: id, the skills it feeds, title, author, URL, and the fetch route when the site blocks a plain GET.
- `sources/<id>.claims.json` holds the claims extracted from one source. Each claim has a verbatim quote, a status, the skill lines that cover it as anchor phrases, and a reason when it is a gap.
- `fetch.py` fetches a source as text. It tries a direct GET first and falls back to the Internet Archive copy.
- `matrix.py` checks every quote against the fetched text, resolves every anchor to a line, asks Jev three questions per claim, and writes the matrix.
- `transcripts.py` reads the Claude Code transcripts on this machine. In debug mode it lists what the human typed after a skill fired and classifies each message into debug-retro's kinds. In lens mode it reads what the human did with a rewrite: ran it, edited it, or dropped it.
- `behave.py` runs a fresh headless Claude on a fixed case with the skill text of a given tree inlined, then grades the trace with Jev.
- `cases/` holds the fixed cases: the latency bug from the copyconstruct post and two lens tasks.
- `report.py` assembles one report from a run directory. `run.sh` runs everything.
- `runs/` is ignored by git. Fetched source texts and run outputs live there.

Jev is TypeSafe's judgment model, reached through the sensibility plugin's judge skill. The skills themselves never call it. Set `JUDGE_PY` if the judge script is not at its default path.

## How a release audit runs

1. `sh audit/run.sh` fetches the sources, runs every claims file against `skills/`, classifies the transcripts, runs the behavioural cases, and writes `audit/runs/<date>/report.md`. Add `--quick` to skip the behavioural runs.
2. Read the re-check list in the report. A claim marked covered that Jev reads below 0.5, or a gap it reads above, is a cell to look at, not a verdict to copy.
3. Read the flagged transcript messages. A kind that appears in two releases running is a line to add.
4. Add lines, re-run, and paste the report into the GitHub release body.

## Adding a source

1. Add an entry to `sources/sources.json` and run `python3 audit/fetch.py --all audit/sources/sources.json audit/runs/sources/`.
2. Read the fetched text in full. Extraction is the reader's job, not a script's: write `sources/<id>.claims.json` with one claim per technique, warning or mistake, each with one verbatim quote.
3. For each claim, name the skill lines that cover it by an anchor phrase unique to the line, or mark it `gap`, `partial`, `infra` or `rejected` with a reason. A line enters a skill only if it would have changed an outcome in a real session or in a behavioural run; a `rejected` claim records why not.
4. Run `matrix.py` for the source. It exits non-zero while a quote or an anchor does not resolve.

## The behavioural rubric

`behave.py` grades a trace against the skill's own definitions, not against a stricter ideal. The first rubric in the v0.4.0 audit asked the lenses for things their text does not promise, no report section and a standing condition in the prompt, and failed 4 of 6 runs that were correct by the skill. The rubric now says that measurements, checks and a findings report are not new deliverables, and asks `/higher` for the history check its text requires. Change a rubric only to match a line in the skill; change the skill when a run shows a real miss.

## Reading Jev's numbers

`covered` is the probability that the cited lines instruct the agent to do what the claim says. `doable` is whether an agent with a shell and read-only production access can do it alone. `specificity` runs from 1, no instruction, to 5, an action with a trigger and a done condition. Jev reads words literally: a claim phrased as an outcome or a counterfactual scores low even when the lines cover the action. Rephrase the claim as the action and judge again before you change a line.
