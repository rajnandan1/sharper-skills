# Audit of three skills against the source post, 2026-10-25

This audit checks `debugging-by-constraints`, `debug-retro` and `signal-first-plan` against Cindy Sridharan's post "How to effectively debug when you no longer understand the code" (copyconstruct, 2026-10-10, https://copyconstruct.medium.com/how-to-effectively-debug-when-you-no-longer-understand-the-code-bd3dcb2c5f7b). The question it answers: does each technique, warning and mistake in the post that a coding agent can act on have a line in a skill, and do the lines stop the mistakes this agent made in its own sessions?

## Sources

- The post. Medium's Cloudflare front returned 403 to curl and the Chrome extension was not connected, so the text came from two raw copies: the Internet Archive capture of 2026-10-17 (16,392 words, the `<article>` element) and the post's own RSS feed entry (16,057 words). Every quote below is verbatim from the archive copy.
- The three skill files from this repo at the commit before this audit.
- Session transcripts under `~/.claude/projects/`: 37 sessions where `debugging-by-constraints` or `signal-first-plan` fired, 30 of them with human messages in the window before the next unrelated slash command.

## Method

1. Extract every technique, warning and mistake in the post as a claim with one quote. 52 claims.
2. Map each claim to the skill lines that cover it, or mark it a gap with a reason.
3. Ask Jev (TypeSafe's judgment model, through the judge skill) three questions per claim with the claim and the covering lines as state: covered, doable by an agent alone, and specificity on a 1 to 5 scale. A Jev answer that disagreed with the matrix was re-checked, not overruled.
4. Classify the 135 human-typed transcript messages with Jev into debug-retro's six kinds plus question and other, then read every non-decision message.
5. Run a fresh subagent on the post's latency bug with the skill before the fixes and again after.
6. Add one line per gap and per recurring transcript mistake, re-judge the changed cells, and re-run the subagent.

## Results

### Coverage

| Status | Claims |
|---|---|
| Covered before the audit | 41 |
| Gap, now fixed | 7 (C3, C6, C8, C27, C47, C48, C52) |
| Partial, now fixed | 2 (C37, C49) |
| Infrastructure the skill cannot provide | 2 (C40 graduated production access, C43 always-on collection) |

Jev agreed with the matrix on 44 of the 51 original cells. It read two covered cells as partial, C28 arithmetic on counts and C36 reviewer citations; both re-checks found the lines cover the action, and they stand. The eleven cells below 0.5 before the fixes were the seven gaps, the two partials, the two infrastructure items, plus C28 and C36.

After the fixes, Jev reads nine of the eleven fixed cells at 0.93 to 0.98 covered. Two stay low on the original claim wording: C37 at 0.09 and C47 at 0.42. Both are a wording effect, not a coverage gap. With the same skill lines and the claim rephrased as the action the agent takes, Jev reads C37 at 0.93, C46 at 0.95 and C47 at 0.97. C37's quote says "adversarial reviews" and the skill says "a fresh subagent given REVIEWER.md"; Jev does not connect the two words. C47's claim is a counterfactual about the post's bug, not an instruction.

### Transcript interventions

135 human-typed messages in 30 sessions, after the harness's injected text was removed. Jev's counts, with the six pasted screenshots counted as proxy:

| Kind | Count |
|---|---|
| decision | 60 |
| question | 32 |
| method | 25 |
| fact | 9 |
| proxy | 10 |
| constraint | 2 |
| other | 3 |

Four mistake kinds recur and the skills did not stop them. Each now has a line.

| Mistake the agent made | Sessions | Line added |
|---|---|---|
| Gathered facts in one folder or one repo and missed recent changes by another team | 2 | debugging-by-constraints Step 0 item 3: list every change in the window across every repo, folder and team |
| Reasoned from a screenshot or a number the human pasted from a dashboard | 3 | Step 0 item 4: a screenshot or pasted number is a lead; re-gather it from the source |
| Asked the human to do something it could try itself | 1 | Step 0 item 4: try it yourself once and show the attempt before asking |
| Committed generated test screenshots into a feature PR | 1 | signal-first-plan Step 4 item 4: list every file in the diff; generated files stay out |

Not changed: access only the human had, such as a browser login or a CVE form, in 2 sessions. debug-retro already turns those into missing-access follow-ups.

### Subagent runs on the post's latency bug

Pass criteria: a control named, a hypotheses-by-fact matrix, the strongest signal named, every claim citing a fact number.

| Run | Control | Matrix | Strongest signal | Citations | Result |
|---|---|---|---|---|---|
| Before the fixes | 3 controls, flag off/off as A | 9 rows by 8 facts | DNS answers 5 against 400, p99 marked weak | every claim cited, 3 uncited mechanism steps listed as ? facts | PASS |
| After the fixes | same host, flag off, with its two-difference caveat named | 10 rows by 8 facts | DNS answers 5 against 400, p99 marked weak | every claim cited, inferences listed under reviewer item 7 | PASS |

The before run did not repeat the post's mistake: it killed the certificate-reload rows on the handshake fact. It did pick a different winning row than the post. It chose fan-out to 400 connections over the post's cause, wrong-shard routing with server-side forwarding, because it read "pre-production showed no change" as a hard contradiction of the routing row. The post says scale was the condition the cause showed under, not a second cause. That is claim C52, which the audit had missed, and Step 2 now says a fact from a smaller scale contradicts a row only if the row's effect does not depend on scale.

The after run shows the new lines in effect. It ran the reviewer items at the end of Step 1 and Step 2, not only at Step 3. It listed the missing change list for the window as a fact to gather. And it kept the wrong-shard routing row alive with a ? on the pre-production fact and named the server-side forward counter that would settle it, instead of killing the post's real cause. It still picked connection fan-out as the winning row and said in plain words that the facts do not separate the two mechanisms, which is what the skill asks for when they do not.

## Lines added

See the diff at the end. In short:

- debugging-by-constraints: capture volatile evidence before an approved restart; a local stack is a repro, not a fact source; keep the fact list and matrix in one working file and re-read it; list every change in the window across teams; throwaway scripts to gather facts; screenshots and pasted numbers are leads; try before asking the user; read code at the bug's version and name the commit; gather the same fact from several instances; check the control by its own value; a reviewer subagent at the end of Step 1 and Step 2 as well as Step 3; scale is a condition, not a second cause.
- debug-retro: a pasted screenshot or quoted dashboard number counts as proxy.
- signal-first-plan: past-bug signals that touch an exit become checks; after deploy, compare production-only signals with the previous successful run; list every file in the diff before commit.

## Claims

- **C1** A control is a case identical to the broken case except for the one suspected difference, such as the same code with the feature flag disabled.
  Quote: “identical to the variable except for the one thing you suspect is causing the bug”
- **C2** Every hypothesis the agent pursues must start from a high-fidelity signal, not from a guess.
  Quote: “Every hypothesis an agents thinks is worth pursuing should start from a high-fidelity signal.”
- **C3** The agent should write throwaway tooling, such as scripts, benchmarks or performance tests, on demand to gather or count facts, because that is an agentic strength.
  Quote: “Very adept at writing throwaway tooling (shell scripts, benchmark tests, performance tests etc) on demand”
- **C4** The agent must not build narratives on thin or non-existent evidence.
  Quote: “They often build baseless narratives out of thin or non-existent evidence.”
- **C5** The agent must not fixate on an obscure edge case and attribute the reported bug to it.
  Quote: “They can fixate on abstruse edge cases”
- **C6** The agent must not walk past its own previous best findings; findings must stay in view across the investigation.
  Quote: “walk past their own previous best findings”
- **C7** Reading the code first to form hypotheses is an anti-pattern; the agent collects all available evidence first and reads code last, only to explain the facts.
  Quote: “reading the code first to formulate hypotheses about a bug should always be the very last resort of the agentic investigation process, not the starting point”
- **C8** When the agent reads code, it chooses which snapshot of the code to read, and a wrong choice misleads it; the code read must be the version that ran when the bug occurred.
  Quote: “the agent decides what snapshot of the code to read. An agent choosing poorly can lead to it making incorrect deductions.”
- **C9** Debugging is a constraint satisfaction problem: the agent must find the one hypothesis consistent with every fact, not any plausible one.
  Quote: “it now needs to find the hypothesis that is fully consistent with every constraint on the table”
- **C10** Gather facts from every available source: logs, crash reports, stack traces, profiles, telemetry, traces, kernel and DNS data, configs, flag values, versions, deploy history, version control history.
  Quote: “collect data from every possible source available to us, such as error logs, crash reports, stack traces, profiler data, telemetry data”
- **C11** Facts are immutable; the agent never alters or disputes them, and when a fact looks suspect it has it gathered again by whoever produced it.
  Quote: “The facts are immutable, and not something an agent can alter or dispute.”
- **C12** Hypotheses are where the agent is most convincing and most often wrong, so they get the most scrutiny and must stay tethered to facts.
  Quote: “A hypothesis is only as strong as the facts underpinning it”
- **C13** A multi-cause hypothesis must satisfy every fact as a whole, and each cause must be strictly necessary: removing it leaves some fact unexplained.
  Quote: “each cause must be strictly necessary, and removing it from the combination should leave some fact unexplained”
- **C14** Never explain away inconvenient facts with a more complicated hypothesis.
  Quote: “the goal should never be to explain away inconvenient facts by coming up with more complicated hypotheses”
- **C15** Do not validate every possible hypothesis; steer to the one most likely to satisfy every fact and test it first.
  Quote: “The goal isn’t to validate every possible hypothesis”
- **C16** A data point present in the variable and absent in the control is a signal; one present in both is noise; noise still eliminates hypotheses built on it but never points anywhere.
  Quote: “If the same data point shows up in both the control and the variable (the TCP handshake time), it’s just noise”
- **C17** Without a control the agent cannot tell signals from noise, so it must obtain a control before steering.
  Quote: “Without a control, an agent can’t tell which of the many promising data points in the sea of facts are signals.”
- **C18** For tricky bugs use a sad-path control that also fails but in a different, louder way; it is often the cheapest because it already exists in the data.
  Quote: “A better control in such cases is often a “sad path” that is also failing, but in a different, louder way than the variable.”
- **C19** A control is only as good as the confidence that it is not broken in the same way as the variable.
  Quote: “a control is only as good as your confidence that it isn’t broken in the same way as the variable”
- **C20** A signal is strong when few hypotheses satisfy it, ideally one; SLOs, SLIs and p99 are usually weak signals.
  Quote: “A signal is considered strong when very few hypotheses satisfy it. Ideally, the number we’re looking for is 1.”
- **C21** Build a hypotheses-by-fact matrix and read it column by column, counting how many hypotheses each signal fits, to find the signal worth pursuing.
  Quote: “generating a matrix which maps every plausible hypothesis to every high-fidelity signal, and count how many hypotheses each signal is consistent with”
- **C22** Read the matrix row by row; a hypothesis is valid only if no fact contradicts it; no all-✓ row means the hypothesis set is wrong.
  Quote: “None of the hypotheses satisfied all three facts (no row in this matrix is all ✓), which was a sign that something was wrong with the current crop of hypotheses.”
- **C23** When every hypothesis falls short, apply five tactics in order before a new hypothesis: reverify how facts were gathered, split coarse hypotheses, merge fine ones, combine complementary ones, then a new hypothesis built only from facts.
  Quote: “Before reaching for a brand new hypothesis, an agent should try some cheaper tactics on for size first.”
- **C24** Progressive signal discovery: start with the cheapest data, go one layer down only when every signal is weak or every hypothesis still falls short, and stop at the first strong signal.
  Quote: “We should stop descending as soon as a strong signal emerges. The goal is to find the strongest signal, not the deepest one.”
- **C25** Validate the candidate hypothesis against every fact, noise included; one contradicting fact discards it.
  Quote: “we need to validate it against every constraint in the factual tier, including the noise”
- **C26** When too few facts exist several hypotheses survive and cannot be told apart; the answer is to gather more facts, not to pick one.
  Quote: “When too few facts are available, several hypotheses survive, and the agent has no way to tell them apart.”
- **C27** Gather the same type of data from several instances of the same bug, such as packet captures from different users or profiles from different hosts; a pattern that repeats across instances and is absent in the control is a real signal.
  Quote: “same type of data from different instances of the same bug”
- **C28** Turn signal isolation into arithmetic: compare counts such as bytes, files opened, DNS lookups, RPCs, time to first byte between control and variable.
  Quote: “letting the arithmetic subsequently guide the agent’s reasoning”
- **C29** Keep the factual tier fat and the derivative tier thin; a fat set of surviving hypotheses means too few or too weak constraints.
  Quote: “A fat derivative tier indicates that an agent is toying with too many hypotheses”
- **C30** A repro is a hypothesis; it counts only if it shows the same strongest signal as the real bug; otherwise it is a different bug and plays no further part.
  Quote: “A repro proves that a bug exists, but not that it is the bug under investigation.”
- **C31** When the report contains repro steps, run them first instead of reading code.
  Quote: “I was as surprised as anyone else when Claude did not first try to reproduce the bug, but instead offered a wrong analysis based on reading the code.”
- **C32** Use the bug report's own facts as constraints before generating hypotheses: first bad and last good version, config defaults, the profile's frame.
  Quote: “What pruned the derivative tier was imposing the constraints already in the bug report”
- **C33** An adversarial reviewer cannot vouch for the completeness of the facts and, with the same context, is one opinion counted twice; use it to eliminate, never to confirm, and keep the main agent's narrative out of it.
  Quote: “two agents concurring can be seen as one opinion counted twice”
- **C34** At the signal step the reviewer checks whether signals also appear in the control, whether the control is broken the same way, and how each fact was gathered.
  Quote: “The adversarial reviewer should first check if the high-fidelity signals also show up in the control.”
- **C35** At the hypothesis step the reviewer estimates how many hypotheses satisfy each signal, checks that tactics 2 to 4 were tried before a new hypothesis, and that a layer descent happened only after that.
  Quote: “the adversarial reviewer should estimate how many hypotheses satisfy each signal, without pursuing any of them”
- **C36** At the validation step the reviewer finds one unsatisfied fact, requires citations for every claim and culls uncited ones, and tests each cause of a combined hypothesis for necessity.
  Quote: “Requiring citations is a practical way to achieve this.”
- **C37** Adversarial review runs at every step of the loop, not only at the end.
  Quote: “Adversarial reviews should be incorporated into every step of the debugging process described above.”
- **C38** Count human interventions per bug; each one is a gap where the agent should have procured a control, a constraint or a check itself; the target is zero.
  Quote: “The number of human interventions per bug is the most honest measure of how “agent-native” a factory really is”
- **C39** Give the agent raw data, because aggregation destroys the signal; reserve decision points for humans and turn each decision into future policy.
  Quote: “Aggregation — the thing that makes a dashboard useful to a human — is often the thing that destroys the value of the signal for an agent.”
- **C40** Agent access to production is read-only by default, scoped to the investigation, time-limited, rate-limit aware, privacy-scrubbed and auditable.
  Quote: “read-only by default, scoped to the current investigation, time-limited, load and rate limit aware, privacy-scrubbed, and auditable”
- **C41** Decisions that carry accountability, such as rollback, escalation or dropping a feature, and choices between fixes with different tradeoffs go to a human, presented unambiguously with the agent's reasoning.
  Quote: “The agent’s job in such cases is to present all available choices to the human in an unambiguous way, along with its reasoning.”
- **C42** Design the verification loop before code is written: decide which quantitative signals would show the feature works or broke, and make the strongest signals available at the shallowest layer by default.
  Quote: “had the application layer logged the number of DNS lookups it was doing, the strongest signal would’ve been available directly from Layer 1”
- **C43** Collect data by default rather than on demand, for example always-on advanced data gathering from a subset of production hosts.
  Quote: “having “always on” advanced data gathering from a small subset of production hosts”
- **C44** Never use the human as a proxy to run commands or paste output; the agent runs them itself, and a human is involved only at a decision, which then becomes policy.
  Quote: “A large number of developers have devolved into being mindless meat proxies”
- **C45** The agent must set up a control, reproduce, constrain hypotheses by the report's facts, and cite claims without being asked; these are mandatory steps, not things a skilled human prompts for.
  Quote: “It didn’t set up a control in the “latency bug” until I asked it to.”
- **C46** Testing and deploy gating should check parity of every high-fidelity signal against the previous successful run, not only pass or fail, and signals from past debugging sessions should become gate checks.
  Quote: “checking for parity when it comes to every high-fidelity signal”
- **C47** A signal learned in a past incident, such as the DNS lookup count, would have caught the regression in pre-production even at small scale if compared with the previous successful run.
  Quote: “if the pre-production testing environment had checked that the client’s DNS lookups matched those on the previous successful run, the routing bug would’ve been caught before it reached production”
- **C48** Prefer facts from the production environment where the bug is observed over an elaborate local harness; a full stack in a box cannot replicate the factual tier.
  Quote: “It’s much more effective to ensure your debugging agent has the all the facts it requires directly from the production environment where the bug is observed, rather than spin up elaborate local test harnesses.”
- **C49** Restarting a process wipes volatile evidence such as stacks and IPC state; capture it before any restart.
  Quote: “which wiped clean any evidence I might’ve been able to gather from a daemon caught dead to rights”
- **C50** When a design rule was violated, such as a single-use state machine reused from a cache, add a test that enforces the rule.
  Quote: “none that enforced that it could never be used in a process wide cache”
- **C51** When another team rebuffs a report for lack of logs, descend layers for harder evidence and re-file with it rather than stop.
  Quote: “I was then able to file a new, comprehensive bug report with the authentication team again with the newfound evidence.”
- **C52** Scale or load can be the condition under which a single cause shows; a fact gathered at a smaller scale does not contradict a hypothesis whose effect grows with scale.
  Quote: “The bug only hurt at production scale, but scale was the condition under which the cause showed up, not a second cause.”

## Matrix

Line numbers are against the files after this audit. "Jev covered" is the probability that the cited lines instruct the agent to do what the claim says, before and after the fix. "doable" is whether a coding agent can do it alone. Specificity: 1 is no instruction, 5 is an action with a trigger and a done condition.

| # | Claim | Status | debugging-by-constraints | debug-retro | signal-first-plan | Jev covered before | after fix | doable | specificity 1 to 5 |
|---|---|---|---|---|---|---|---|---|---|
| C1 | A control is a case identical to the broken case except for the one suspected difference, such as the same code with the feature flag disabled. | covered | SKILL.md:39 | - | - | 0.96 | same | 0.28 | 3.8 |
| C2 | Every hypothesis the agent pursues must start from a high-fidelity signal, not from a guess. | covered | SKILL.md:60, SKILL.md:68 | - | - | 0.74 | same | 0.62 | 4.7 |
| C3 | The agent should write throwaway tooling, such as scripts, benchmarks or performance tests, on demand to gather or count facts, because that is an agentic strength. | gap | SKILL.md:?, SKILL.md:32 (added) | - | - | 0.13 | 0.95 | 0.74 | 2.5 to 4.6 |
| C4 | The agent must not build narratives on thin or non-existent evidence. | covered | SKILL.md:75, SKILL.md:16 | - | - | 0.90 | same | 0.58 | 4.8 |
| C5 | The agent must not fixate on an obscure edge case and attribute the reported bug to it. | covered | SKILL.md:76 | - | - | 0.60 | same | 0.68 | 4.7 |
| C6 | The agent must not walk past its own previous best findings; findings must stay in view across the investigation. | gap | SKILL.md:62, SKILL.md:24 (added) | - | - | 0.09 | 0.95 | 0.67 | 3.1 to 4.7 |
| C7 | Reading the code first to form hypotheses is an anti-pattern; the agent collects all available evidence first and reads code last, only to explain the facts. | covered | SKILL.md:10, SKILL.md:? | - | - | 0.89 | same | 0.69 | 4.3 |
| C8 | When the agent reads code, it chooses which snapshot of the code to read, and a wrong choice misleads it; the code read must be the version that ran when the bug occurred. | gap | SKILL.md:15, SKILL.md:29, SKILL.md:33 (added) | - | - | 0.14 | 0.94 | 0.40 | 3.1 to 4.6 |
| C9 | Debugging is a constraint satisfaction problem: the agent must find the one hypothesis consistent with every fact, not any plausible one. | covered | SKILL.md:18 | - | - | 0.95 | same | 0.33 | 3.7 |
| C10 | Gather facts from every available source: logs, crash reports, stack traces, profiles, telemetry, traces, kernel and DNS data, configs, flag values, versions, deploy history, version control history. | covered | SKILL.md:14, LAYERS.md:11-19 | - | - | 0.81 | same | 0.35 | 3.3 |
| C11 | Facts are immutable; the agent never alters or disputes them, and when a fact looks suspect it has it gathered again by whoever produced it. | covered | SKILL.md:14, SKILL.md:63 | - | - | 0.96 | same | 0.41 | 4.0 |
| C12 | Hypotheses are where the agent is most convincing and most often wrong, so they get the most scrutiny and must stay tethered to facts. | covered | SKILL.md:16, SKILL.md:75 | - | - | 0.84 | same | 0.52 | 4.6 |
| C13 | A multi-cause hypothesis must satisfy every fact as a whole, and each cause must be strictly necessary: removing it leaves some fact unexplained. | covered | SKILL.md:18, SKILL.md:77 | - | - | 0.96 | same | 0.33 | 5.0 |
| C14 | Never explain away inconvenient facts with a more complicated hypothesis. | covered | SKILL.md:18, SKILL.md:67 | - | - | 0.85 | same | 0.48 | 3.7 |
| C15 | Do not validate every possible hypothesis; steer to the one most likely to satisfy every fact and test it first. | covered | SKILL.md:60 | - | - | 0.76 | same | 0.63 | 4.1 |
| C16 | A data point present in the variable and absent in the control is a signal; one present in both is noise; noise still eliminates hypotheses built on it but never points anywhere. | covered | SKILL.md:43 | - | - | 0.73 | same | 0.48 | 2.5 |
| C17 | Without a control the agent cannot tell signals from noise, so it must obtain a control before steering. | covered | SKILL.md:39, SKILL.md:47 | - | - | 0.78 | same | 0.51 | 4.8 |
| C18 | For tricky bugs use a sad-path control that also fails but in a different, louder way; it is often the cheapest because it already exists in the data. | covered | SKILL.md:41 | - | - | 0.97 | same | 0.56 | 4.2 |
| C19 | A control is only as good as the confidence that it is not broken in the same way as the variable. | covered | SKILL.md:45, SKILL.md:45 (added) | - | - | 0.93 | 0.93 | 0.39 | 3.1 to 4.7 |
| C20 | A signal is strong when few hypotheses satisfy it, ideally one; SLOs, SLIs and p99 are usually weak signals. | covered | SKILL.md:60 | - | - | 0.92 | same | 0.44 | 4.1 |
| C21 | Build a hypotheses-by-fact matrix and read it column by column, counting how many hypotheses each signal fits, to find the signal worth pursuing. | covered | SKILL.md:51, SKILL.md:60 | - | - | 0.92 | same | 0.52 | 4.4 |
| C22 | Read the matrix row by row; a hypothesis is valid only if no fact contradicts it; no all-✓ row means the hypothesis set is wrong. | covered | SKILL.md:61, SKILL.md:62 | - | - | 0.82 | same | 0.56 | 4.3 |
| C23 | When every hypothesis falls short, apply five tactics in order before a new hypothesis: reverify how facts were gathered, split coarse hypotheses, merge fine ones, combine complementary ones, then a new hypothesis built only from facts. | covered | SKILL.md:62-67 | - | - | 0.95 | same | 0.58 | 4.5 |
| C24 | Progressive signal discovery: start with the cheapest data, go one layer down only when every signal is weak or every hypothesis still falls short, and stop at the first strong signal. | covered | SKILL.md:27, SKILL.md:68, LAYERS.md:3 | - | - | 0.92 | same | 0.53 | 4.6 |
| C25 | Validate the candidate hypothesis against every fact, noise included; one contradicting fact discards it. | covered | SKILL.md:74 | - | - | 0.89 | same | 0.56 | 4.2 |
| C26 | When too few facts exist several hypotheses survive and cannot be told apart; the answer is to gather more facts, not to pick one. | covered | SKILL.md:61, SKILL.md:70, SKILL.md:68 | - | - | 0.93 | same | 0.60 | 4.8 |
| C27 | Gather the same type of data from several instances of the same bug, such as packet captures from different users or profiles from different hosts; a pattern that repeats across instances and is absent in the control is a real signal. | gap | SKILL.md:42, SKILL.md:44 (added) | - | - | 0.28 | 0.70 | 0.46 | 3.7 to 4.4 |
| C28 | Turn signal isolation into arithmetic: compare counts such as bytes, files opened, DNS lookups, RPCs, time to first byte between control and variable. | covered | SKILL.md:42 | - | - | 0.41 | same | 0.59 | 3.6 |
| C29 | Keep the factual tier fat and the derivative tier thin; a fat set of surviving hypotheses means too few or too weak constraints. | covered | SKILL.md:18, SKILL.md:68 | - | - | 0.80 | same | 0.50 | 4.2 |
| C30 | A repro is a hypothesis; it counts only if it shows the same strongest signal as the real bug; otherwise it is a different bug and plays no further part. | covered | SKILL.md:76 | - | - | 0.91 | same | 0.37 | 4.9 |
| C31 | When the report contains repro steps, run them first instead of reading code. | covered | SKILL.md:30 | - | - | 0.95 | same | 0.73 | 4.6 |
| C32 | Use the bug report's own facts as constraints before generating hypotheses: first bad and last good version, config defaults, the profile's frame. | covered | SKILL.md:29 | - | - | 0.66 | same | 0.57 | 4.2 |
| C33 | An adversarial reviewer cannot vouch for the completeness of the facts and, with the same context, is one opinion counted twice; use it to eliminate, never to confirm, and keep the main agent's narrative out of it. | covered | SKILL.md:78, REVIEWER.md:7 | - | - | 0.93 | same | 0.65 | 4.8 |
| C34 | At the signal step the reviewer checks whether signals also appear in the control, whether the control is broken the same way, and how each fact was gathered. | covered | REVIEWER.md:11-13 | - | - | 0.89 | same | 0.53 | 3.8 |
| C35 | At the hypothesis step the reviewer estimates how many hypotheses satisfy each signal, checks that tactics 2 to 4 were tried before a new hypothesis, and that a layer descent happened only after that. | covered | REVIEWER.md:14-15 | - | - | 0.85 | same | 0.49 | 4.8 |
| C36 | At the validation step the reviewer finds one unsatisfied fact, requires citations for every claim and culls uncited ones, and tests each cause of a combined hypothesis for necessity. | covered | REVIEWER.md:16-18, SKILL.md:75 | - | - | 0.35 | same | 0.44 | 4.5 |
| C37 | Adversarial review runs at every step of the loop, not only at the end. | partial | SKILL.md:78, REVIEWER.md:3 (added) | - | - | 0.22 | 0.09 | 0.54 | 4.6 to 4.7 |
| C38 | Count human interventions per bug; each one is a gap where the agent should have procured a control, a constraint or a check itself; the target is zero. | covered | - | SKILL.md:9, SKILL.md:42 | - | 0.91 | same | 0.40 | 4.5 |
| C39 | Give the agent raw data, because aggregation destroys the signal; reserve decision points for humans and turn each decision into future policy. | covered | SKILL.md:60 | SKILL.md:35 | SKILL.md:34 | 0.79 | same | 0.34 | 4.3 |
| C40 | Agent access to production is read-only by default, scoped to the investigation, time-limited, rate-limit aware, privacy-scrubbed and auditable. | infra | SKILL.md:22, SKILL.md:25 | - | - | 0.17 | same | 0.17 | 4.0 |
| C41 | Decisions that carry accountability, such as rollback, escalation or dropping a feature, and choices between fixes with different tradeoffs go to a human, presented unambiguously with the agent's reasoning. | covered | SKILL.md:90 | - | - | 0.98 | same | 0.06 | 4.5 |
| C42 | Design the verification loop before code is written: decide which quantitative signals would show the feature works or broke, and make the strongest signals available at the shallowest layer by default. | covered | - | SKILL.md:36 | SKILL.md:10, SKILL.md:42 | 0.84 | same | 0.29 | 4.7 |
| C43 | Collect data by default rather than on demand, for example always-on advanced data gathering from a subset of production hosts. | infra | - | - | SKILL.md:42 | 0.44 | same | 0.18 | 3.8 |
| C44 | Never use the human as a proxy to run commands or paste output; the agent runs them itself, and a human is involved only at a decision, which then becomes policy. | covered | SKILL.md:? | SKILL.md:?, SKILL.md:35 | - | 0.97 | same | 0.70 | 4.5 |
| C45 | The agent must set up a control, reproduce, constrain hypotheses by the report's facts, and cite claims without being asked; these are mandatory steps, not things a skilled human prompts for. | covered | SKILL.md:29, SKILL.md:30, SKILL.md:39, SKILL.md:75 | - | - | 0.85 | same | 0.53 | 4.8 |
| C46 | Testing and deploy gating should check parity of every high-fidelity signal against the previous successful run, not only pass or fail, and signals from past debugging sessions should become gate checks. | covered | - | - | SKILL.md:43, SKILL.md:51-52, SKILL.md:35, SKILL.md:53 (added) | 0.53 | 0.57 | 0.30 | 4.8 to 4.4 |
| C47 | A signal learned in a past incident, such as the DNS lookup count, would have caught the regression in pre-production even at small scale if compared with the previous successful run. | gap | - | - | SKILL.md:42, SKILL.md:51, SKILL.md:53 (added) | 0.35 | 0.42 | 0.33 | 3.8 to 3.3 |
| C48 | Prefer facts from the production environment where the bug is observed over an elaborate local harness; a full stack in a box cannot replicate the factual tier. | gap | SKILL.md:23, SKILL.md:76, SKILL.md:23 (added) | - | - | 0.63 | 0.93 | 0.55 | 4.4 to 3.9 |
| C49 | Restarting a process wipes volatile evidence such as stacks and IPC state; capture it before any restart. | partial | SKILL.md:22, SKILL.md:22 (added) | - | - | 0.24 | 0.98 | 0.12 | 3.6 to 4.0 |
| C50 | When a design rule was violated, such as a single-use state machine reused from a cache, add a test that enforces the rule. | covered | - | SKILL.md:33 | - | 0.92 | same | 0.55 | 4.4 |
| C51 | When another team rebuffs a report for lack of logs, descend layers for harder evidence and re-file with it rather than stop. | covered | SKILL.md:68, SKILL.md:90 | - | - | 0.60 | same | 0.46 | 4.8 |
| C52 | Scale or load can be the condition under which a single cause shows; a fact gathered at a smaller scale does not contradict a hypothesis whose effect grows with scale. | gap | SKILL.md:61, SKILL.md:61 (added) | - | - | 0.21 | 0.95 | 0.35 | 3.4 to 4.4 |

## Diff

```diff
diff --git a/skills/debug-retro/SKILL.md b/skills/debug-retro/SKILL.md
index 77c6109..a71cf53 100644
--- a/skills/debug-retro/SKILL.md
+++ b/skills/debug-retro/SKILL.md
@@ -17,7 +17,7 @@ Read this conversation from the start of the debug session. An intervention is a
 | control | gave a comparison case, or asked the agent to set one up |
 | fact | supplied data, or pointed at data the agent had not gathered |
 | constraint | pushed back with a fact that killed a hypothesis |
-| proxy | ran a command or pasted output the agent could have run itself |
+| proxy | ran a command, pasted output or a screenshot, or quoted a dashboard number the agent could have read itself |
 | method | told the agent how to work: run the repro, cite, split the hypothesis, go a layer down |
 | decision | picked a fix, or made a rollback, escalation or scope call |
 
diff --git a/skills/debugging-by-constraints/REVIEWER.md b/skills/debugging-by-constraints/REVIEWER.md
index f3ecb96..5c7b5d7 100644
--- a/skills/debugging-by-constraints/REVIEWER.md
+++ b/skills/debugging-by-constraints/REVIEWER.md
@@ -1,6 +1,6 @@
 # Reviewer brief
 
-Pass this file to a fresh subagent with: the numbered fact list with sources and code facts, the control and variable, and the hypotheses-by-fact matrix with its winning row. Leave out the main agent's narrative and the code it read.
+Pass this file to a fresh subagent with: the numbered fact list with sources and code facts, the control and variable, and the hypotheses-by-fact matrix with its winning row. Leave out the main agent's narrative and the code it read. The review runs three times: items 1 to 3 at the end of Step 1, items 4 and 5 at the end of Step 2, and all eight items at Step 3. A new subagent each time.
 
 ---
 
diff --git a/skills/debugging-by-constraints/SKILL.md b/skills/debugging-by-constraints/SKILL.md
index bd54b05..8b03391 100644
--- a/skills/debugging-by-constraints/SKILL.md
+++ b/skills/debugging-by-constraints/SKILL.md
@@ -19,16 +19,18 @@ Each fact is a _constraint_. The job is to find the one hypothesis (a single cau
 
 ## Guardrails
 
-- Production is read-only for you. Ask the user before any command that restarts, scales, writes, deletes, or flips a flag.
-- Before you start an app locally, find what it calls out to on start (seed data, schedulers, health checks, webhooks) and turn those off first.
+- Production is read-only for you. Ask the user before any command that restarts, scales, writes, deletes, or flips a flag. Before a restart you get approval for, capture what it destroys: thread stacks, open connections, IPC state, a memory profile.
+- Before you start an app locally, find what it calls out to on start (seed data, schedulers, health checks, webhooks) and turn those off first. A local stack is a repro, which Step 3 treats as a hypothesis. It is never a source of facts for the matrix; gather facts from where the bug happened.
+- Keep the numbered fact list and the matrix in one working file and update it in place. A new fact takes the next number. Nothing is renumbered or dropped. Re-read the file before you add a hypothesis or change the winning row, so no earlier finding is walked past. A finding that is not in the file does not exist.
 - Write `<REDACTED>` in place of every secret in commands, outputs and artifacts you show. Quote only the lines that carry the signal.
 
 ## Step 0: Gather facts, cheapest first
 
 1. Read the bug report in full. Turn everything in it into numbered facts: first bad and last good version, config, flags, symptoms, attached profiles and logs.
 2. If the report has repro steps, run them now and record the signal they produce.
-3. Run every query and command yourself. [LAYERS.md](LAYERS.md) names the MCP server or CLI that reaches each layer 1 source. `.claude/debug-layers.md` at the project root lists the sources and signals past sessions in this codebase found; read it first when it exists. The user is a source of last resort: ask only for data no tool reaches, and name the exact command, file, host and time window you need.
-4. Read code to explain the bug only after this, and only to explain facts you hold. Record what you find as code facts. Reading code to start the app or build a repro (schema, seed data, config) is setup, and you can do it at any step.
+3. List every change in the window between last good and first bad, across every repo, folder and team that touches the path: commits, deploys, config, flag flips, dependency bumps. A change by another team is still a fact.
+4. Run every query and command yourself. [LAYERS.md](LAYERS.md) names the MCP server or CLI that reaches each layer 1 source. `.claude/debug-layers.md` at the project root lists the sources and signals past sessions in this codebase found; read it first when it exists. When no tool reaches a fact, write a throwaway script to gather or count it, and name the script as the fact's source. A screenshot, a pasted number or a dashboard reading is a lead, not a fact: re-gather it from its source with the exact query and time window, and record that as the fact. The user is a source of last resort: before you ask them to run, open or check anything, try it yourself once and show the attempt; then ask only for data no tool reaches, and name the exact command, file, host and time window you need.
+5. Read code to explain the bug only after this, and only to explain facts you hold. Read it at the version that ran when the bug occurred, the first bad version from the report, and name that commit in each code fact; HEAD is a different program. Reading code to start the app or build a repro (schema, seed data, config) is setup, and you can do it at any step.
 
 Done when a numbered fact list exists and every fact names its source: the tool and query, the file, or the report line.
 
@@ -39,9 +41,10 @@ The **variable** is the broken case. The **control** is a case equal to it excep
 - When the happy path differs from the variable in too many ways, pick a _sad path_ control: a case that also fails, but in a different and louder way (an auth error that does log, next to a hang that logs nothing). It often already sits in the data you have.
 - Gather the same facts from both. Compare them as numbers wherever you can: DNS answers, connections, RPCs, retries, bytes, files opened, stack frames.
 - A data point in the variable and not in the control is a **signal**. One in both is **noise**. Noise points nowhere, but it still kills any hypothesis built on it.
-- Check that the control is not broken the same way. A control with the same bug turns every signal into noise.
+- Gather the same fact from several instances of the variable: other hosts, users or requests that show the bug. A signal that one instance shows and the others do not is a quirk of that instance, not the bug.
+- Check that the control is not broken the same way: gather the control's own value for the reported symptom and show that it is healthy. A control with the same bug turns every signal into noise.
 
-Done when every fact is tagged signal or noise, and the one difference between control and variable is written down.
+Done when every fact is tagged signal or noise, the one difference between control and variable is written down, and a fresh subagent given [REVIEWER.md](REVIEWER.md) items 1 to 3, the fact list and the control has found no signal that also sits in the control, no way the control is broken the same way, and no fact without its host, time window and tool.
 
 ## Step 2: Build the matrix
 
@@ -55,7 +58,7 @@ H3 server CPU throttled     ✓              ✗                       ✓
 ```
 
 - **Read the columns.** A signal that fits almost every row is _weak_. Aggregates such as p99, error rate and SLOs usually are. A signal that fits one row is _strong_. Steer to the row the strongest signal points at, and test that row first.
-- **Read the rows.** One ✗ kills a row. A ? is a fact to gather, not a pass.
+- **Read the rows.** One ✗ kills a row. A ? is a fact to gather, not a pass. A fact from a smaller scale, a different configuration or a different load contradicts a row only if the row's effect does not depend on that condition. Scale is the condition a cause shows under, not a second cause: mark such a cell ? and name the fact at the variable's scale that would settle it.
 - **No row is all ✓?** Apply these in order, and rebuild the matrix after each one:
   1. Re-check how the suspect fact was gathered: host, time window, version, tool.
   2. Split a coarse hypothesis ("the deploy did it") into its parts.
@@ -64,7 +67,7 @@ H3 server CPU throttled     ✓              ✗                       ✓
   5. Only then propose a new hypothesis, built from the facts.
 - **Every signal weak, or tactic 5 finds nothing?** Go one layer down in [LAYERS.md](LAYERS.md): down the stack for an infrastructure bug, down the request path for a logic bug. Run Step 0 for that layer. Stop at the first layer that gives a strong signal. Gather more facts, not more hypotheses.
 
-Done when exactly one row is ✓ in every cell, with no ?, and a strong signal points at it.
+Done when exactly one row is ✓ in every cell, with no ?, a strong signal points at it, and a fresh subagent given [REVIEWER.md](REVIEWER.md) items 4 and 5 and the matrix has agreed on which signals are weak and found no tactic you skipped before a new hypothesis or a layer descent.
 
 ## Step 3: Validate
 
@@ -72,7 +75,7 @@ Done when exactly one row is ✓ in every cell, with no ?, and a strong signal p
 - **Cite.** Every claim in your explanation names the fact number it rests on. A claim with no fact is removed, or becomes a fact to gather.
 - **Repro parity.** A repro is a hypothesis. It counts only when it shows the same strongest signal as the real bug: the same frame in the heap profile, the same packet sequence, the same count. A repro with a different signal is a different bug. Drop it. With no production data, the reported symptom is the signal to match.
 - **Necessity.** For a combined row (one hypothesis with two or more causes), remove each cause in turn. Some fact must go unexplained each time, or that cause is not needed.
-- **Review.** Dispatch a fresh subagent with [REVIEWER.md](REVIEWER.md), the fact list with its code facts, the control, and the matrix. Leave out your narrative and the code you read. Its job is to break the winning row. A reviewer cannot see a fact nobody gathered, so its agreement proves nothing; only a contradiction counts. If it finds one, go back to Step 2.
+- **Review.** Dispatch a fresh subagent with all eight items of [REVIEWER.md](REVIEWER.md), the fact list with its code facts, the control, and the matrix. Leave out your narrative and the code you read. Its job is to break the winning row. A reviewer cannot see a fact nobody gathered, so its agreement proves nothing; only a contradiction counts. If it finds one, go back to Step 2.
 
 Done when:
 
diff --git a/skills/signal-first-plan/SKILL.md b/skills/signal-first-plan/SKILL.md
index 0d0d912..c38343e 100644
--- a/skills/signal-first-plan/SKILL.md
+++ b/skills/signal-first-plan/SKILL.md
@@ -32,7 +32,7 @@ A signal is a number that a broken version changes: DNS lookups per request, row
 - On a response exit, count over the whole body the client receives (the serialized page data or JSON), not over the one field you expect to carry the data. A leak sits in the field nobody planned for.
 - A number that the working and the broken version share is noise. Pick another.
 - Aggregates such as p99 and error rate are weak, because many causes move them. Prefer a count tied to one exit.
-- Read `.claude/debug-layers.md` at the project root, when it exists, for signals that past bugs needed.
+- Read `.claude/debug-layers.md` at the project root, when it exists, for signals that past bugs needed. Each one that touches an exit of this feature becomes a check in Step 3.
 
 Done when every exit has a signal and an expected value for every case.
 
@@ -50,4 +50,6 @@ Show the user the plan as a table, then build: exit, signal, expected value per
 
 1. After you build, run every check on main and on the branch.
 2. List each signal that changed. Every change must be one the plan expected. Fix any other change before merge.
-3. In the PR, give the exit table and the comparison.
+3. For a signal that only production or pre-production can show, compare its value in the first environment after deploy with the same signal on that environment's previous successful run, not with an absolute threshold and not only with pass or fail. This applies to every signal in the plan, including the ones taken from `.claude/debug-layers.md`. The post's DNS lookup count differed from the previous successful run even at pre-production scale, so this check would have caught that bug before production.
+4. Before you commit, list every file in the diff. Generated files, such as test screenshots and attachments, stay out unless the plan named them.
+5. In the PR, give the exit table and the comparison.
```
