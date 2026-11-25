<picture>
  <source media="(prefers-color-scheme: dark)" srcset="brand/sharper-skills-horizontal-white.svg">
  <img alt="sharper-skills" src="brand/sharper-skills-horizontal.svg" width="480">
</picture>

Eight skills for coding agents. Six make the agent more precise before it acts. One does open-ended creative work. One checks that you understand what it did. Each skill is a folder with a `SKILL.md` file. Any agent that reads that format can use it: Claude Code, Codex, Cursor, OpenCode, Gemini CLI, GitHub Copilot, and others. `/leonardo` does the task itself. The other seven shape the prompt, the plan, the investigation, the next session, or your understanding of the change.

## The skills

The first three skills are prompt lenses. Each lens rewrites your task. It then hands the new prompt back to you. You reply `go` to run it. The lenses come from Felix Rieseberg's post "How to be more ambitious: A tutorial for humans with models".

- `/higher <task>` rewrites a task to ask for the outcome one level up. Two examples are the decision instead of the deck, and "keep the apps crash-free" instead of "fix this crash".
- `/deeper <task>` rewrites a task to use what a top professional in the field would use. That means the rawest inputs, named instruments, and a check outside the model.
- `/wider <task>` rewrites a task to use the methods of other fields. It also names a red team that attacks the result.

The other three skills work from evidence. They come from copyconstruct's post "How to effectively debug when you no longer understand the code".

- `signal-first-plan` runs before you build a feature. It lists every exit the feature's data leaves through. It puts a countable signal on each exit. It checks the signals against main, the branch before your change. The agent invokes it on its own when you ask for behaviour that ships to users or other systems.
- `debugging-by-constraints` runs on production bugs and review findings. It gathers facts first. It picks a control, a case that is equal to the broken one except for the suspected difference. It builds a matrix of hypotheses against facts. It keeps the one hypothesis that fits every fact. The agent invokes it on its own. You can also run `/debugging-by-constraints`.
- `/debug-retro` runs after a debug session. It counts each time you had to step in. It turns each one into a lasting rule. It has had the least use so far.

The next skill does the work itself. It comes from creativity research, listed under Sources.

- `/leonardo <task>` does an open-ended task, such as a name, a concept, copy or a design. It aims to beat the default: the answer the agent gives to the bare task with no method. The agent writes a short brief and the criteria that make one candidate better than another. Then it starts subagents, which are separate agent runs that see only what they are given. One subagent writes the default. Five each write 4 candidates with one move. A move is a thinking method, such as invert the problem or drop an assumption. Two judge subagents score all 21 answers without knowing which one is the default. The 3 top-scoring candidates that are different ideas each get one redraft, and two new judges score them again. You get the winner, the 2 runners-up, the default and the scores. That makes 13 subagents, plus a third judge in a round where two judges disagree by 2 points or more. In 4 test runs in Claude Code on 2026-11-25, on a tool name, a farewell poem and an app feature, a run took 10 to 15 minutes and cost $7.70 to $11.20 by Claude Code's own cost report. A plain answer to the same task took about 20 seconds and $0.40.

The method follows three findings: more attempts give more good results (Jung et al.), people who work alone and pool their ideas beat brainstorming groups (Diehl and Stroebe), and a varied set of good drafts finds the best one better than aiming straight at it (Stanley and Lehman). The loop of draft, judge and redraft is what Ken Kocienda calls creative selection at Apple: demo, feedback, next demo. The moves come from Claude Shannon's 1952 talk "Creative Thinking".

The last skill checks you, not the agent. It comes from Addy Osmani's post "Critical thinking when agents do the work".

- `/defend` runs after a session or a change. It writes an HTML report on what the session decided and changed: the context, the intuition, each decision with who made it and the evidence behind it, and, for code, the existing code the change relies on. Questions at the bottom ask you to reason with the work, starting with the decisions you agreed to in a quick reply. You answer in your own words, and the agent grades each answer against a rubric it wrote first. The pass mark is every answer right. What you do next, such as a merge, is your call.

## Install

Pick one of the three ways.

### Any agent, one skill at a time

The `skills` CLI from Vercel Labs installs skills from a GitHub repo into the folder your agent reads. Its source is https://github.com/vercel-labs/skills. It needs Node.js 22.20 or later. Run it from your project:

```
npx skills add rajnandan1/sharper-skills
```

The CLI lists the eight skills and the agents it finds on your machine. You pick the skills and the agents you want. The CLI installs the skills into the current project. Add `-g` to install them for every project.

To skip the prompts, name the skills and the agents:

```
npx skills add rajnandan1/sharper-skills --list
npx skills add rajnandan1/sharper-skills --skill deeper -a claude-code
npx skills add rajnandan1/sharper-skills --skill debugging-by-constraints --skill debug-retro -a codex -a cursor -g
```

`npx skills update` pulls new versions later. `npx skills remove deeper` removes one skill.

### Claude Code, all eight as a plugin

1. Run `/plugin marketplace add rajnandan1/sharper-skills`.
2. Run `/plugin install sharper-skills@sharper-skills`.

When you install the plugin, each skill also answers to its prefixed name, such as `/sharper-skills:higher`.

### By hand

Copy the whole folder of each skill you want from `skills/` into the folder your agent reads. The folders of `deeper`, `higher`, `wider`, `leonardo`, `defend` and `debug-retro` hold an `agents/` folder for Codex; copy it too (see Start a skill).

- Claude Code reads `~/.claude/skills/`.
- Codex reads `~/.agents/skills/`.
- Cursor reads `~/.cursor/skills/`.

## Start a skill

To start a skill yourself, type its name and then the task, such as `/deeper add retry logic`. Codex uses `$deeper` instead of `/deeper`. If you type only the name, the three lenses (`deeper`, `higher`, `wider`) and `leonardo` work on your last message in the conversation, and `defend` works on everything the conversation produced.

`signal-first-plan` and `debugging-by-constraints` also start on their own when your task matches their description. The other six, `deeper`, `higher`, `wider`, `leonardo`, `defend` and `debug-retro`, are meant to start only when you type their name. Claude Code and Cursor wait for you because of the `disable-model-invocation: true` line at the top of each of those six `SKILL.md` files. Codex waits because of the `agents/openai.yaml` file in each of those six skill folders. The OpenCode, Hermes and Gemini CLI agents have no such setting, so their model can start one of the six unasked. `defend` writes an HTML report and a rubric file, and `debug-retro` writes rules to a file under `~/.sharper-skills/`, so an unasked start can leave files you did not ask for. `leonardo` starts many subagents, so an unasked start can spend far more tokens than you planned. You can still install the six in those agents. To rule out unasked starts there, install only the other two: `npx skills add rajnandan1/sharper-skills --skill signal-first-plan --skill debugging-by-constraints`.

## Where learned rules go

`debug-retro` writes the sources, signals and decisions it learns about a codebase to `~/.sharper-skills/<project>/debug-layers.md`, outside the repo. `<project>` is the `origin` remote URL in lowercase as `host/owner/repo`, such as `github.com/rajnandan1/sharper-skills`, so every clone and worktree of a repo shares one file. A repo with no remote uses the path of its main checkout, the folder that holds its `.git` folder. Finding the main checkout needs git 2.31 or later. A folder outside git uses its own path. The file stays on your machine, so teammates and your other machines do not share it. `debugging-by-constraints` and `signal-first-plan` read that file when it exists. `debug-retro` leaves your repos and the skill files unchanged, so a plugin update does not lose your rules. Rules about the method itself go to an issue or pull request in `rajnandan1/sharper-skills`.

If a repo still has `.claude/debug-layers.md` from an older version of `debug-retro`, run this from the repo root to move it into place. The block's first four lines set `$store` the same way the skills do. If a store file already exists, `mv -n` leaves both files as they are, and you merge the old lines by hand. If the old file was committed, commit its removal too.

```sh
key=$(git remote get-url origin 2>/dev/null | sed -E 's#^[a-z+]+://##; s#^[^@/]*@##; s#:[0-9]+/#/#; s#:#/#; s#\.git$##; s#/$##; s#\.\.#_#g' | tr 'A-Z' 'a-z')
[ -n "$key" ] || key=$(git rev-parse --path-format=absolute --git-common-dir 2>/dev/null | sed 's#/\.git$##')
[ -n "$key" ] || key=$(pwd -P)
store="$HOME/.sharper-skills/${key#/}"
mkdir -p "$store" && mv -n .claude/debug-layers.md "$store/debug-layers.md"
```

`skills/debugging-by-constraints/LAYERS.md` lists the tools that reach each layer of facts. Its layer 1 table shows the author's stack as an example: Grafana, Prometheus, Railway, PostHog, ClickHouse, kubectl. Replace each tool with the one that reaches the same fact in your stack.

## Sources

- Felix Rieseberg, "How to be more ambitious: A tutorial for humans with models": https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/
- copyconstruct, "How to effectively debug when you no longer understand the code": https://copyconstruct.medium.com/how-to-effectively-debug-when-you-no-longer-understand-the-code-bd3dcb2c5f7b
- Addy Osmani, "Critical thinking when agents do the work": https://x.com/addyosmani/status/2117512471930167377
- Ken Kocienda, *Creative Selection* (2018): https://panmacmillan.com/authors/ken-kocienda/creative-selection/9781529004731
- Kenneth Stanley and Joel Lehman, *Why Greatness Cannot Be Planned* (2015): https://www.springer.com/gp/book/9783319155234
- Claude Shannon, "Creative Thinking" (1952): https://jamesclear.com/great-speeches/creative-thinking-by-claude-shannon
- Jung et al., "Quantity yields quality when it comes to creativity" (2015): https://pmc.ncbi.nlm.nih.gov/articles/PMC4479710
- Diehl and Stroebe, "Productivity Loss in Brainstorming Groups: Toward the Solution of a Riddle" (1987): https://homepages.se.edu/cvonbergen/files/2013/01/Productivity-Loss-In-Brainstorming_Toward-the-Solution-of-a-Riddle.pdf


## License

MIT.
