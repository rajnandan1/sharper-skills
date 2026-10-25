---
name: wider
description: Rewrite a task to bring in the methods of other fields. /wider <task>, or /wider alone for your last request.
argument-hint: "[task]"
disable-model-invocation: true
---

# /wider

Method source: Felix Rieseberg, "How to be more ambitious: A tutorial for humans with models", https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/

Bring other fields into this task:

$ARGUMENTS

If the task above is empty, the task is the user's most recent request in this conversation.

Wider means the task gets the methods of fields it would not normally afford: the analyst, the journalist, and the editor on one deck, and a short seller to attack it. Same deliverable. Methods, not characters: ask for what a short seller does to research a position, never for a short seller to play. The output of this skill is a prompt, not the task's result.

## 1. Answer three questions

Under these three headings in this order:

- **Verbs**: the task restated as what it does to whom, with no noun for the artifact. A quarterly review is not a deck. It is "getting busy people to believe a story about cause and effect, and to decide under uncertainty, in 30 minutes". One or two sentences.
- **Crew**: three to five fields whose practitioners do those verbs at the top level, and for each the one method from that field that applies here. One line per field. At least one field is one the task would not normally afford. Pick for the medium too: a result that is presented gets a field that works in the room.
- **Red team**: one field whose job is to find the hole in this kind of result, and what its practitioner would do to this result. One or two sentences.

Done when each field carries a method specific enough to run on this task, not a title.

## 2. Rewrite the prompt

Write the prompt the user should have sent: it asks for the same deliverable, done with the crew's methods and attacked by the red team's method before the user sees it. Each method is written as what to do, not who to be. When the fields can work apart, the prompt says so, so each can run as its own subagent. Keep the user's facts, names, and numbers verbatim. Put it in one fenced code block.

## 3. Hand it back

Output is the three headings, the code block and this closing line: "Reply `go` to run it, or edit it first. Other lenses: `/higher` if a meeting will discuss this, `/deeper` if it must be right." Running the rewrite is the user's call.
