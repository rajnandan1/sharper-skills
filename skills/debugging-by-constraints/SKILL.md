---
name: debugging-by-constraints
description: Evidence-first debugging for production bugs and PR review findings. Use when a bug or performance regression shows up in production telemetry, a user bug report, or a reviewer's or review bot's PR comment, starts after a deploy or version change, has no fast local repro, or sits in code the agent did not write. Use it before you offer fix options.
---

# Debugging by constraints

Method source: copyconstruct, "How to effectively debug when you no longer understand the code" (2026-10-10), https://copyconstruct.medium.com/how-to-effectively-debug-when-you-no-longer-understand-the-code-bd3dcb2c5f7b

Code is an _unreliable narrator_: it says what can happen, not what did happen. Start from what did happen.

The work sits on two tiers:

- **Facts** are data a tool or a person gathered: the bug report, logs, metrics, traces, config, flag values, versions, deploy history, git history, profiles, packet and DNS data. Docs, help text, specs and existing tests are facts about intended behaviour. You read facts. You never edit or argue them away. A fact that looks wrong gets gathered again, or goes back to whoever produced it.
- **Code facts** record what the code says, with its location (`C3: incidents.ts:480 groups rows with groupByIdKeepAll`). Code says only what can happen, so a code fact can explain a mechanism but never serves as the strongest signal.
- **Hypotheses** are everything you infer: causes, theories, narratives, and every repro you build. A repro becomes a source of facts once it shows the reported symptom. A hypothesis lives only while it fits every fact.

Each fact is a _constraint_. The job is to find the one hypothesis (a single cause, or a combination where every cause is needed) that fits every fact. Keep the facts fat and the hypotheses thin.

## Guardrails

- Production is read-only for you. Ask the user before any command that restarts, scales, writes, deletes, or flips a flag.
- Before you start an app locally, find what it calls out to on start (seed data, schedulers, health checks, webhooks) and turn those off first.
- Write `<REDACTED>` in place of every secret in commands, outputs and artifacts you show. Quote only the lines that carry the signal.

## Step 0: Gather facts, cheapest first

1. Read the bug report in full. Turn everything in it into numbered facts: first bad and last good version, config, flags, symptoms, attached profiles and logs.
2. If the report has repro steps, run them now and record the signal they produce.
3. Run every query and command yourself. [LAYERS.md](LAYERS.md) names the MCP server or CLI that reaches each layer 1 source. `.claude/debug-layers.md` at the project root lists the sources and signals past sessions in this codebase found; read it first when it exists. The user is a source of last resort: ask only for data no tool reaches, and name the exact command, file, host and time window you need.
4. Read code to explain the bug only after this, and only to explain facts you hold. Record what you find as code facts. Reading code to start the app or build a repro (schema, seed data, config) is setup, and you can do it at any step.

Done when a numbered fact list exists and every fact names its source: the tool and query, the file, or the report line.

## Step 1: Pick a control, find the signals

The **variable** is the broken case. The **control** is a case equal to it except for the suspected difference: flag off, last good version, a healthy host, an unaffected user. When no good version exists because the bug is older than the report, pick the control inside the same version: a record, user or request that does not show the bug.

- When the happy path differs from the variable in too many ways, pick a _sad path_ control: a case that also fails, but in a different and louder way (an auth error that does log, next to a hang that logs nothing). It often already sits in the data you have.
- Gather the same facts from both. Compare them as numbers wherever you can: DNS answers, connections, RPCs, retries, bytes, files opened, stack frames.
- A data point in the variable and not in the control is a **signal**. One in both is **noise**. Noise points nowhere, but it still kills any hypothesis built on it.
- Check that the control is not broken the same way. A control with the same bug turns every signal into noise.

Done when every fact is tagged signal or noise, and the one difference between control and variable is written down.

## Step 2: Build the matrix

List the plausible hypotheses. Then draw the hypotheses-by-fact matrix: one row per hypothesis, one column per fact (signals and noise), and in each cell ✓ fits, ✗ contradicts, or ? unknown.

```
                         F1 p99 up   F2 DNS answers 5 → 400   F3 handshake same in both
H1 cert reload per RPC      ✓              ✗                       ✓
H2 client skips sharding    ✓              ✓                       ✓
H3 server CPU throttled     ✓              ✗                       ✓
```

- **Read the columns.** A signal that fits almost every row is _weak_. Aggregates such as p99, error rate and SLOs usually are. A signal that fits one row is _strong_. Steer to the row the strongest signal points at, and test that row first.
- **Read the rows.** One ✗ kills a row. A ? is a fact to gather, not a pass.
- **No row is all ✓?** Apply these in order, and rebuild the matrix after each one:
  1. Re-check how the suspect fact was gathered: host, time window, version, tool.
  2. Split a coarse hypothesis ("the deploy did it") into its parts.
  3. Merge fine hypotheses that each explain one host or one instance into the shared cause.
  4. Combine two hypotheses that each explain different facts and contradict none.
  5. Only then propose a new hypothesis, built from the facts.
- **Every signal weak, or tactic 5 finds nothing?** Go one layer down in [LAYERS.md](LAYERS.md): down the stack for an infrastructure bug, down the request path for a logic bug. Run Step 0 for that layer. Stop at the first layer that gives a strong signal. Gather more facts, not more hypotheses.

Done when exactly one row is ✓ in every cell, with no ?, and a strong signal points at it.

## Step 3: Validate

- Check the winning row against every fact, noise included.
- **Cite.** Every claim in your explanation names the fact number it rests on. A claim with no fact is removed, or becomes a fact to gather.
- **Repro parity.** A repro is a hypothesis. It counts only when it shows the same strongest signal as the real bug: the same frame in the heap profile, the same packet sequence, the same count. A repro with a different signal is a different bug. Drop it. With no production data, the reported symptom is the signal to match.
- **Necessity.** For a combined row (one hypothesis with two or more causes), remove each cause in turn. Some fact must go unexplained each time, or that cause is not needed.
- **Review.** Dispatch a fresh subagent with [REVIEWER.md](REVIEWER.md), the fact list with its code facts, the control, and the matrix. Leave out your narrative and the code you read. Its job is to break the winning row. A reviewer cannot see a fact nobody gathered, so its agreement proves nothing; only a contradiction counts. If it finds one, go back to Step 2.

Done when:

- [ ] the winning row is ✓ on every fact
- [ ] every claim cites a fact number
- [ ] every repro you relied on shows the strongest signal
- [ ] every cause in a combined row is necessary
- [ ] the reviewer returned no breaking fact

## Step 4: Fix

1. If one fix fits, state it. If more than one fits (remove the cache, or make the state machine safe to re-enter), list each with its tradeoff and your reasoning, and ask the user to pick before you change code. Calls that carry accountability go to the user the same way: roll back, escalate to another team, drop a feature.
2. Check the fix against the intended-behaviour facts. When it changes who sees what, or behaviour those facts describe, match them. Where they are silent or disagree, ask the user.
3. Write a regression test at a seam that shows the real signal. If no seam can show it, say so.
4. Update every doc, help text and test that describes the changed behaviour.
5. Remove every debug probe you added.
6. In the commit or PR, state the cause, the strongest signal, and the control.

## Report

Give the fact list, the matrix, the winning row and its strongest signal. End with: "Run `/debug-retro` to turn each time you stepped in into a rule."
