---
name: defend
description: Turn a session's decisions, or a code change, into an HTML report with questions at the bottom. You answer in your own words, and the agent grades. /defend, or /defend <PR, branch, commit range or topic>.
argument-hint: "[PR, branch, commit range or topic]"
disable-model-invocation: true
---

# /defend

The user wants to understand this work well enough to defend it: to explain each decision, and each line of any code, to the person who will live with it. The main targets are the decisions the user agreed to with a quick "yes": a well-written proposal is easy to accept without a view of one's own. The output is an HTML report with questions at the bottom. The user answers in their own words, and you grade each answer against a rubric you wrote first.

Work: $ARGUMENTS

If the work above is empty, it is everything this conversation produced: the decisions, conclusions and plans it reached, the documents it wrote, and the code it changed. A PR, branch, commit range or topic narrows it. If this conversation produced nothing, the work is the current branch against its base, plus uncommitted work.

## 1. Gather the work

The **request** is what the work set out to do: the user's asks in this conversation, or else the PR body, the commit messages and any linked ticket. Read the conversation from its start, and every source it relied on. When the work includes code, read the full diff, the commit messages, and the PR body and its review threads. Then read the existing code that the change calls into and the code that calls it. Much of the change's behaviour lives there, outside the diff.

List these items. Give each one a **citation**: a file and line in the changed version, a quoted message from this conversation, or a link to a run or a source.

- **Decisions**: each choice the work rests on. Name who made it. A user decision cites the message where the user agreed. An agent decision is one the user never weighed: a default, a scope cut, a requirement reinterpreted where two clashed, an order of operations, or a review suggestion left out. For each one, give the alternative not taken and what it would have cost.
- **Assumptions**: each fact the work relies on that nothing checked.
- **Evidence**: each test, run, measurement, review or source behind a decision, with what it proved and what it left open.
- **Existing paths**, for code: the code outside the diff whose behaviour the change depends on.

Done when every item has a citation, every decision names who made it, and every hunk of a diff maps to a decision or to the request.

## 2. Write the report

Write one self-contained HTML file with inline CSS. Write it for a reader who did not see the work. Use these sections, in this order:

1. **Context**: what was wrong or wanted, who it affects, and why now.
2. **Intuition**: the mental model in plain words, with one diagram or worked example that shows the mechanism.
3. **What was decided and done**: the work in the order that builds understanding. Quote the message where each decision landed, and the lines of code that carry it.
4. **Existing paths**, when the work has code: the code outside the diff that the change relies on, quoted.
5. **Decisions and assumptions**: the lists from step 1, with who made each decision.
6. **Evidence**: what each piece proved and what it left open. For each decision, add what would have to be true for it to be wrong.
7. **Risk**: what breaks if a decision or an assumption is wrong, and the first place to look.
8. **Questions**: the questions from step 3, with no answers.

Done when each section cites the work.

## 3. Write the questions and the rubric

Write at most 8 questions. Pick first the decisions the user agreed to in a short reply and the decisions the agent made alone. Then pick the assumptions and evidence gaps that would cost the most if the reader misread them. When the work has code, add one changed line picked at random, preferring a line of new logic. Each question makes the reader reason with the work: defend a decision against its alternative, say what would have to be true for it to be wrong, predict the outcome on an input, name what a piece of evidence leaves open, or say what breaks without a line.

Then write the **rubric**: for each question, the points that a right answer must contain, each with a citation. Save it next to the report, with the same name ending in `-rubric.md`. It stays out of the page and out of the chat, so the bar is fixed before any answer arrives.

Done when every question has a rubric entry with a citation.

## 4. Hand it over

Save the report in the system temp folder as `defend-<repo or topic>-<yyyymmdd-hhmm>.html`, open it in the browser, and print the full path. Then ask question 1 in the chat.

## 5. Grade

Ask one question at a time, and grade each answer against the rubric:

- **Right**: the answer holds every rubric point, in any words. Quote the line of code or the message that confirms it.
- **Vague**: ask one follow-up that targets the missing point, then grade.
- **Wrong**: name the missing point and the report section to reread. Later, ask a new question on the same decision, because the answer to this one is now known.
- **Disputed**: read the cited code or message again. When the user is right, fix the rubric and say so. Otherwise, quote it.

The pass mark is every question right. Done when the user passes or stops. End with the score and the decisions not yet passed. Acting on the work, such as a merge, is the user's call.
