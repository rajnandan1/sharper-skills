<picture>
  <source media="(prefers-color-scheme: dark)" srcset="brand/sharper-skills-horizontal-white.svg">
  <img alt="sharper-skills" src="brand/sharper-skills-horizontal.svg" width="480">
</picture>

Seven skills for coding agents. Six make the agent more precise before it acts. One checks that you understand what it did. Each skill is a folder with a `SKILL.md` file. Any agent that reads that format can use it: Claude Code, Codex, Cursor, OpenCode, Gemini CLI, GitHub Copilot, and others. None of them does the task. Each one shapes the prompt, the plan, the investigation, the next session, or your understanding of the change.

## The skills

The first three skills are prompt lenses. Each lens rewrites your task. It then hands the new prompt back to you. You reply `go` to run it. The lenses come from Felix Rieseberg's post "How to be more ambitious: A tutorial for humans with models".

- `/higher <task>` rewrites a task to ask for the outcome one level up. Two examples are the decision instead of the deck, and "keep the apps crash-free" instead of "fix this crash".
- `/deeper <task>` rewrites a task to use what a top professional in the field would use. That means the rawest inputs, named instruments, and a check outside the model.
- `/wider <task>` rewrites a task to use the methods of other fields. It also names a red team that attacks the result.

The other three skills work from evidence. They come from copyconstruct's post "How to effectively debug when you no longer understand the code".

- `signal-first-plan` runs before you build a feature. It lists every exit the feature's data leaves through. It puts a countable signal on each exit. It checks the signals against main, the branch before your change. The agent invokes it on its own when you ask for behaviour that ships to users or other systems.
- `debugging-by-constraints` runs on production bugs and review findings. It gathers facts first. It picks a control, a case that is equal to the broken one except for the suspected difference. It builds a matrix of hypotheses against facts. It keeps the one hypothesis that fits every fact. The agent invokes it on its own. You can also run `/debugging-by-constraints`.
- `/debug-retro` runs after a debug session. It counts each time you had to step in. It turns each one into a lasting rule. It has had the least use so far.

The last skill checks you, not the agent. It comes from Addy Osmani's post "Critical thinking when agents do the work".

- `/defend` runs after a change, before you merge. It writes an HTML report on the change: the context, the intuition, what changed, the decisions and assumptions the agent made, and what the checks prove. It also covers the existing code the change relies on. Questions at the bottom ask you to reason with the change. You answer in your own words, and the agent grades each answer against a rubric it wrote first. You merge after every answer is right.

## Install

Pick one of the three ways.

### Any agent, one skill at a time

The `skills` CLI from Vercel Labs installs skills from a GitHub repo into the folder your agent reads. Its source is https://github.com/vercel-labs/skills. It needs Node.js 22.20 or later. Run it from your project:

```
npx skills add rajnandan1/sharper-skills
```

The CLI lists the seven skills and the agents it finds on your machine. You pick the skills and the agents you want. The CLI installs the skills into the current project. Add `-g` to install them for every project.

To skip the prompts, name the skills and the agents:

```
npx skills add rajnandan1/sharper-skills --list
npx skills add rajnandan1/sharper-skills --skill deeper -a claude-code
npx skills add rajnandan1/sharper-skills --skill debugging-by-constraints --skill debug-retro -a codex -a cursor -g
```

`npx skills update` pulls new versions later. `npx skills remove deeper` removes one skill.

Only Claude Code fills in the `<task>` argument. In every other agent, the three lenses take the task from your last message.

### Claude Code, all seven as a plugin

1. Run `/plugin marketplace add rajnandan1/sharper-skills`.
2. Run `/plugin install sharper-skills@sharper-skills`.

When you install the plugin, each skill also answers to its prefixed name, such as `/sharper-skills:higher`.

### By hand

Copy the folders you want from `skills/` into the folder your agent reads:

- Claude Code reads `~/.claude/skills/`.
- Codex reads `~/.agents/skills/`.
- Cursor reads `~/.cursor/skills/`.

## Where learned rules go

`debug-retro` writes what it learns about a codebase to `.claude/debug-layers.md` at that project's root. `debugging-by-constraints` and `signal-first-plan` read that file when it exists. The skill files stay unchanged, so a plugin update does not lose your rules. Rules about the method itself go to an issue or pull request in this repo.

`skills/debugging-by-constraints/LAYERS.md` lists the tools that reach each layer of facts. Its layer 1 table shows the author's stack as an example: Grafana, Prometheus, Railway, PostHog, ClickHouse, kubectl. Replace each tool with the one that reaches the same fact in your stack.

## Sources

- Felix Rieseberg, "How to be more ambitious: A tutorial for humans with models": https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/
- copyconstruct, "How to effectively debug when you no longer understand the code": https://copyconstruct.medium.com/how-to-effectively-debug-when-you-no-longer-understand-the-code-bd3dcb2c5f7b
- Addy Osmani, "Critical thinking when agents do the work": https://x.com/addyosmani/status/2117512471930167377


## License

MIT.
