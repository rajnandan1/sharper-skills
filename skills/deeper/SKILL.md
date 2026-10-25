---
name: deeper
description: Rewrite a task to ask for the deeper version, not the bigger one. /deeper <task>, or /deeper alone to deepen your last request.
argument-hint: "[task]"
disable-model-invocation: true
---

# /deeper

Make this task deeper, not bigger:

$ARGUMENTS

If the task above is empty, the task is the user's most recent request in this conversation.

Deeper means the inputs, methods, and checks a top professional in the field would use. Bigger means more deliverables. The deliverable stays the same. The output of this skill is a prompt, not the task's result.

## 1. Answer four questions

One to three sentences each, specific to this task, under these four headings in this order:

- **Professional**: what a top professional in this field would do here that the task does not ask for, including the finding nobody asked about that the raw material would show.
- **Raw material**: the rawest material they would start from instead of the digested version the task offers. The logs, not the dashboard. The rows, not the chart. The source, not the summary. If the task states a belief, the raw material is what tests it.
- **Instruments**: the specific methods and tools they would use, named well enough to run: the query, the statistic, the library, the command, the procedure.
- **Outside judge**: what, other than the model or the user, would show the result is right: a test that runs, a measurement, held-out data, a second tool. Best: a check the model can run and get an answer from at once.

Done when each heading names something concrete that applies to this task and not to every task.

## 2. Rewrite the prompt

Write the prompt the user should have sent: it asks for exactly the four answers above. Keep the user's goal, facts, names, and numbers verbatim. Same deliverable, same scope. Put it in one fenced code block.

## 3. Hand it back

Output is the four headings, the code block and this closing line: "Reply `go` to run it, or edit it first. Other lenses: `/higher` if a meeting will discuss this, `/wider` if it must be great on several fronts." Running the rewrite is the user's call.
