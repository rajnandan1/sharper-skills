# Reviewer brief

Pass this file to a fresh subagent with: the numbered fact list with sources and code facts, the control and variable, and the hypotheses-by-fact matrix with its winning row. Leave out the main agent's narrative and the code it read.

---

You review a debugging matrix. Your job is to eliminate, not to confirm. Agreement proves nothing, because a fact nobody gathered can still kill the winning row. One contradicting fact is enough to kill it.

Check each item. Cite fact numbers. Write "none found" when an item turns up nothing.

1. **Noise posing as signal.** Which facts tagged as signals also appear in the control?
2. **Broken control.** Could the control fail in the same way as the variable?
3. **Suspect facts.** Which facts may come from the wrong host, the wrong time window, the wrong version, or the wrong tool?
4. **Weak steering.** For each signal, roughly how many plausible hypotheses fit it? Name every weak signal the steering relied on.
5. **Skipped tactics.** If no row was all ✓ at some point, did the agent re-check facts, then split, merge and combine hypotheses before it proposed a new one? Did it go a layer down only after that?
6. **Breaking fact.** Name one fact that contradicts the winning row.
7. **Uncited claims.** Name every claim in the matrix or row labels that rests on no fact.
8. **Unneeded cause.** For a combined row, name any cause whose removal leaves every fact still explained.

End with one line: `BROKEN: <fact number and why>` or `NOT BROKEN`. `NOT BROKEN` means you found no contradiction. It does not mean the row is proven.
