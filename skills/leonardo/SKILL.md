---
name: leonardo
description: Runs only when the user asks for /leonardo by name. Do open-ended work, such as a name, a concept, copy or a design, by making many candidates apart, picking them blind against the plain answer, and redrafting the best. /leonardo <task>, or /leonardo alone for your last request.
argument-hint: "[task]"
disable-model-invocation: true
---

# /leonardo

Do the user's open-ended task and beat the **default**: the answer the same agent gives to the bare task with no method. The task is the text the user typed after the skill's name. Claude Code adds that text at the end of this skill as an `ARGUMENTS:` line. If the user typed nothing after the name, the task is the user's most recent request in this conversation.

The method is creative selection: many candidates made apart, a blind pick against stated taste, the next version of each pick, and another blind pick. Making candidates is cheap. Picking is the hard part, so most of the care goes into the Taste in step 1 and the judges in step 3. The output of this skill is the finished work.

Run the default, every generator, every judge and every redrafter as its own subagent, so its context holds no other candidate, score or move. If you cannot start subagents, run each one as a separate pass and finish it before you start the next.

## 1. Frame

Start the default first and wait for its answer before you write any file, so nothing it can read holds the Brief or the Taste. It gets the user's task text exactly as typed, and nothing else. It returns one answer.

Then write three blocks before any candidate exists:

- **Brief**: the deliverable, who it is for, what it must do for them, and the hard limits: format, length, facts that must stay. Each line traces to the user's words or to a plain fact about the audience. An idea of your own goes into a candidate. Keep the user's facts, names and numbers verbatim.
- **Taste**: 3 to 5 criteria that say which kind of difference makes one candidate better than another for this task. The first is fit: it does the job in the Brief within the limits. Each other criterion says what the difference does for the person in the Brief, such as "a buyer can repeat the name after hearing it once".
- **Moves**: 5 moves from the list below, one per generator, picked to fit the task.

Moves:

1. **Simplify**: strip the problem to its core, solve that, then add back what was cut.
2. **Borrow**: find a solved problem close to this one, in this field or a distant one, and adapt its solution. A distant field enters as a metaphor.
3. **Restate**: rephrase the problem 5 ways, and solve the restatement that surprises you most.
4. **Generalize**: solve the broader class of problems this one belongs to, then fit the answer back.
5. **Split**: break the one big leap into small steps, and take them in order.
6. **Invert**: swap the givens and the goal, or solve for the opposite outcome, then work back.
7. **Drop**: list 3 assumptions this kind of work takes as given that the Brief does not require, and drop a different one in each candidate.
8. **Constrain**: add one annoying constraint that the default would never choose, and meet it.
9. **Seed**: start from one small concrete detail, such as a phrase, a gesture or one screen, and grow the work out of it.

Done when each Taste criterion could not be pasted unchanged into another task.

## 2. Generate apart

In one message, start 5 generators. Each gets the Brief, its one move and the rules below. Generators get the Brief and not the Taste, so they make without judging.

- Work the problem through your own way before you look at any existing answer, example or competitor. Look afterwards only to drop a candidate that copies one.
- Write 4 candidates.
- Write each candidate as the thing itself at working size: the name, the paragraph, the screen, the outline.
- Write every candidate down, the weak-looking ones too. Judging happens later, somewhere else.
- Return each candidate with one line on the idea behind it.

Done when the pool holds 20 candidates, each tagged with its move, plus the default.

## 3. Pick blind

1. Number the pool in a shuffled order, with the default among the candidates, and strip the tags. Keep the key from number to move, or to the default, to yourself.
2. In one message, start 2 judges. Each gets the Brief, the Taste and the numbered pool, and nothing about where any candidate came from. Each judge gives every candidate one whole score from 1 (least) to 5 (best) against the Taste, with one line of reason, ranks its top 3 in order, and lists the candidates that are the same idea in another form.
3. Where the 2 scores for a candidate differ by 2 or more, start a third judge on those candidates and take the median of the 3.
4. Keep 3 **picks**: the highest mean score first, with a tie broken by the judges' ranks, then each next highest that is not the same idea as a pick. A different idea at a lower score is a stepping stone: the next round can grow the best version out of it.

Done when every candidate has its scores and the 3 picks are 3 different ideas.

## 4. Redraft

1. For each pick, start one redrafter. It gets the Brief, the pick and the judges' reasons for it. It makes the next version with one change. It may instead throw the draft out and redo it from the same idea, or change the Brief slightly when that makes the work matter more. It returns the new version, the one change, and its answer to "If this change were already made, would I go back to the old version?" When the answer is yes, it returns the old version.
2. Run step 3 again on a pool of the picks, their new versions and the default, with 2 new judges and the same Taste.

Done when the new judges have scored every version.

## 5. Hand it back

If the default ranked first in the last round, run steps 2 to 4 once more with the moves not used yet, and say so in the hand-back.

Show:

1. The winner in full.
2. The other 2 picks, with one line each on how they differ from the winner.
3. The default in full, and its rank in the last round.
4. A table of the last round: each candidate, its move, and its scores.
5. Each change to the Brief that a redrafter made.

End with this line: "Pick one, or tell me what all three get wrong, and I will run another round with that in the Taste."
