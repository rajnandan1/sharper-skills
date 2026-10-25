---
name: debug-retro
description: After a debug session, count each time you had to step in and turn each one into a lasting rule. /debug-retro
disable-model-invocation: true
---

# /debug-retro

Each time the human stepped in during a debug session, they supplied something the agent could have found alone. Count those steps and give each one a lasting home, so the next session needs fewer. The goal is zero steps per bug.

## 1. List the interventions

Read this conversation from the start of the debug session. An intervention is a human message that did one of these:

| Kind | The human… |
| --- | --- |
| control | gave a comparison case, or asked the agent to set one up |
| fact | supplied data, or pointed at data the agent had not gathered |
| constraint | pushed back with a fact that killed a hypothesis |
| proxy | ran a command, pasted output or a screenshot, or quoted a dashboard number the agent could have read itself |
| method | told the agent how to work: run the repro, cite, split the hypothesis, go a layer down |
| decision | picked a fix, or made a rollback, escalation or scope call |

The original bug report is not an intervention. Decisions are expected, so count them apart from the rest.

Done when every human message in the session is listed with a kind, or skipped as the original report.

## 2. Give each one a home

For each intervention, propose the smallest lasting change that would have let the agent do it alone:

- **control, fact, proxy:** a line in `.claude/debug-layers.md` at the project root. Create the file if it is missing, with the heading `# Debug layers: learned in this codebase`. Give the source, the exact query or command, and the signal it showed. If no tool could reach the data, name the missing access (an MCP server, a read-only credential) as a follow-up for the user.
- **constraint:** the fact that should be gathered by default, written as above. If the missing piece was a design rule in the code ("this state machine is single-use"), name a test that would enforce it as a follow-up in the repo.
- **method:** check the debugging-by-constraints SKILL.md first. If the skill lacks the rule, propose the rule. If the skill has it and the agent skipped it, the wording is too weak: propose sharper wording for that line. The home is an issue or pull request at https://github.com/rajnandan1/sharper-skills with the exact line, because the installed skill files belong to the plugin and an update overwrites them.
- **decision:** a policy line in the project `CLAUDE.md` or a feedback memory, only when the call will come up again ("roll back a slow but correct feature when p99 doubles for 15 minutes"). A one-off call stays one-off.
- **a signal that took a layer descent to find:** a follow-up for the codebase that names the log line or metric to emit by default, so the next session finds it at layer 1.

## 3. Show, then write

Print:

1. `Interventions this session: N (plus D decisions).`
2. A table: number, kind, what the human said (quoted), proposed home, exact text to add.
3. The follow-ups that need the user or the repo.

Ask the user to approve the rows by number. Write only the approved rows. Before you add a line, check that the target file does not already say the same thing; update the existing line instead of adding a second one.

Done when every intervention is written, rejected by the user, or listed as a follow-up.
