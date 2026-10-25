---
name: signal-first-plan
description: Signal-first planning before you build a feature. Lists every exit the feature's data leaves through, puts a countable signal on each, and checks the signals against main. Use when the user asks to build, add or change behaviour that ships to users or other systems. Skip it for questions, explanations, bug hunts, refactors with no behaviour change, and copy or style edits.
---

# Signal-first plan

Method source: copyconstruct, "How to effectively debug when you no longer understand the code" (2026-10-10), https://copyconstruct.medium.com/how-to-effectively-debug-when-you-no-longer-understand-the-code-bd3dcb2c5f7b. Its latency bug reached production because no check compared the client's DNS lookup count with the last good run.

Before you build, decide how you will see that the feature works and how you will see that it broke. A feature breaks at its _exits_: the places where its data or behaviour leaves the process. Name every exit, put one _signal_ on each, and make every signal checkable before you write the feature.

A small change can have one exit. Then the plan is one row.

## Step 1: List the exits

An exit is any place where the feature's data or behaviour leaves the process:

- responses: rendered pages, page data, API bodies, redirects, status codes
- messages: emails, webhooks, notifications, feeds, sitemaps, badges, embeds
- outbound calls: HTTP, DNS, queues, third-party APIs
- writes: database rows, files, caches, logs

Trace exits from the data, not from the files you plan to change. Start at each table, column, flag or config value the feature reads or changes. Follow every query, controller, route and job that reads it, out to the place where it leaves the process. A reader you did not plan to touch is still an exit.

Done when every reader of the touched data is in the list as an exit, or is marked internal with a reason.

## Step 2: Put one signal on each exit

A signal is a number that a broken version changes: DNS lookups per request, rows written per job, payment API calls per checkout, emails sent per signup.

- Write the expected value for every case the feature splits on: each type of viewer, each input class, each config value.
- On a response exit, count over the whole body the client receives (the serialized page data or JSON), not over the one field you expect to carry the data. A leak sits in the field nobody planned for.
- A number that the working and the broken version share is noise. Pick another.
- Aggregates such as p99 and error rate are weak, because many causes move them. Prefer a count tied to one exit.
- Read `.claude/debug-layers.md` at the project root, when it exists, for signals that past bugs needed.

Done when every exit has a signal and an expected value for every case.

## Step 3: Make every signal checkable

- Prefer a test that reaches the exit the way a client does and asserts the signal. One test can loop over many exits and cases.
- When only production can show the signal (latency, call counts at real scale), emit it where the stack already logs or measures. A later debug session then finds it at layer 1.
- Run the checks on main. A check for new behaviour fails there. A check for behaviour the feature must keep passes there. If a keep check fails on main, the bug already exists: report it to the user before you build on top of it.

Done when every signal has a test or an emitted metric, and you know which checks pass on main.

Show the user the plan as a table, then build: exit, signal, expected value per case, check (test name or metric), result on main.

## Step 4: Compare before merge

1. After you build, run every check on main and on the branch.
2. List each signal that changed. Every change must be one the plan expected. Fix any other change before merge.
3. In the PR, give the exit table and the comparison.
