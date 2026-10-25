---
name: higher
description: Rewrite a task to ask for the goal beyond the goal. /higher <task>, or /higher alone for your last request.
argument-hint: "[task]"
disable-model-invocation: true
---

# /higher

Method source: Felix Rieseberg, "How to be more ambitious: A tutorial for humans with models", https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/

Raise this task one level, from the task to the outcome it serves:

$ARGUMENTS

If the task above is empty, the task is the user's most recent request in this conversation.

A task is the user's best guess at how to get an outcome. Higher means asking for the outcome instead: the decision instead of the deck, the standing condition instead of the one-off fix, "keep the apps crash-free" instead of "fix this crash". Each call climbs one rung; the user runs `/higher` on the result to climb again. The output of this skill is a prompt, not the task's result.

If the task has no outcome beyond itself, such as creative work or a one-off with nothing above it, say so in one line and stop. `/deeper` is the lens for that task.

## 1. Answer four questions

One to three sentences each, specific to this task, under these four headings in this order:

- **Purpose**: why this task exists, what it is for, and who acts on it. "The review exists so leadership catches problems early and moves money and people to the right places."
- **Beyond**: what the user wants to happen after this task is done. The goal beyond the goal.
- **Standing condition**: the outcome stated as something that stays true, so the model can own it without a new request each time. "Crash-free", not "fix this crash".
- **Access**: what the model needs to own that outcome end to end: the data, the systems, the machines, the mapping from symptom to cause. Name what exists today and what the user must set up.

Done when each heading names something concrete that applies to this task and not to every task.

## 2. Rewrite the prompt

Write the prompt the user should have sent: it names the purpose in its first sentence and asks for the outcome one level up. Doing it covers the original task or makes it unnecessary. Keep the user's facts, names, and numbers verbatim. Where history exists, the prompt asks to show the new way would have worked on it. Put it in one fenced code block.

## 3. Hand it back

Output is the four headings, the code block and this closing line: "Reply `go` to run it, or edit it first. Other lenses: `/deeper` if it must be right, `/wider` if it must be great on several fronts." Running the rewrite is the user's call.
