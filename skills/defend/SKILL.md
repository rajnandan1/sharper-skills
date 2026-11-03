---
name: defend
description: Turn a change into an HTML report with questions at the bottom. You answer in your own words, and the agent grades. /defend, or /defend <PR, branch or commit range>.
argument-hint: "[PR, branch or commit range]"
disable-model-invocation: true
---

# /defend

The user wants to understand this change well enough to defend it: to explain each line and each decision to the person who will maintain it. The output is an HTML report with questions at the bottom. The user answers in their own words, and you grade each answer against a rubric you wrote first.

Change: $ARGUMENTS

If the change above is empty, it is the work of this conversation: the commits and uncommitted edits it made. If this conversation made none, it is the current branch against its base, plus uncommitted work.

## 1. Gather the change

The **request** is what the change set out to do: the user's ask in this conversation, or else the PR body, the commit messages and any linked ticket. Read the full diff, every commit message, and the PR body and its review threads when a PR exists. Then read the existing code that the change calls into and the code that calls it. Much of the change's behaviour lives there, outside the diff.

List four things. Give each item a file and line in the changed version:

- **Decisions**: each choice the request did not dictate. Examples are a default, a scope cut, a requirement reinterpreted where two clashed, an order of operations, an error path, a new dependency, and a review suggestion left out. For each one, give the alternative not taken and what it would have cost.
- **Assumptions**: each fact the change relies on that no check proved.
- **Checks**: each test, CI run, review, measurement or screenshot that ran on the change, with what it proved and what it left open.
- **Existing paths**: the code outside the diff whose behaviour the change depends on.

Done when every hunk of the diff maps to a decision or to the request, and every item names its file and line.

## 2. Write the report

Write one self-contained HTML file with inline CSS. Write it for a reader who did not see the work. Use these sections, in this order:

1. **Context**: what was wrong or wanted, who it affects, and why now.
2. **Intuition**: the mental model in plain words, with one diagram or worked example that shows the mechanism.
3. **Existing paths**: the code outside the diff that the change relies on, quoted.
4. **What changed**: the diff in the order that builds understanding, not file order. Quote the lines that carry each point.
5. **Decisions and assumptions**: the lists from step 1.
6. **Checks**: what each check proved and what it left open.
7. **Risk**: what breaks if a decision or an assumption is wrong, and the first place to look.
8. **Questions**: the questions from step 3, with no answers.

Done when each section cites the diff, the existing code or a check.

## 3. Write the questions and the rubric

Write at most 8 questions. Pick the decisions, assumptions and check gaps that would cost the most if the reader misread them. Add one line of new logic, picked at random from the diff. Each question makes the reader reason with the change: predict the outcome on an input, defend a decision against its alternative, name what a check leaves open, or say what breaks without a line.

Then write the **rubric**: for each question, the points that a right answer must contain, each cited to a file and line. Save it next to the report, with the same name ending in `-rubric.md`. It stays out of the page and out of the chat, so the bar is fixed before any answer arrives.

Done when every question has a rubric entry with a citation.

## 4. Hand it over

Save the report in the system temp folder as `defend-<repo>-<yyyymmdd-hhmm>.html`, open it in the browser, and print the full path. Then ask question 1 in the chat.

## 5. Grade

Ask one question at a time, and grade each answer against the rubric:

- **Right**: the answer holds every rubric point, in any words. Quote the line of code that confirms it.
- **Vague**: ask one follow-up that targets the missing point, then grade.
- **Wrong**: name the missing point and the report section to reread. Later, ask a new question on the same decision, because the answer to this one is now known.
- **Disputed**: read the cited code again. When the user is right, fix the rubric and say so. Otherwise, quote the line.

The pass mark is every question right. Done when the user passes or stops. End with the score and the decisions not yet passed. The merge is the user's call.
