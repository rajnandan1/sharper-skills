# sharper-skills

Six skills for coding agents that make the agent more precise before it acts. Each skill is a folder with a `SKILL.md` file, so it works in any agent that reads that format: Claude Code, Codex, Cursor, OpenCode, Gemini CLI, GitHub Copilot and others. None of them does the task. Each one shapes the prompt, the plan, the investigation, or the next session.

## The skills

Three prompt lenses. Each one rewrites a task and hands the prompt back. You reply `go` to run it. The lenses come from Felix Rieseberg's post "How to be more ambitious: A tutorial for humans with models".

- `/higher <task>` rewrites a task to ask for the outcome one level up: the decision instead of the deck, "keep the apps crash-free" instead of "fix this crash".
- `/deeper <task>` rewrites a task to use what a top professional in the field would use: the rawest inputs, named instruments, and a check outside the model.
- `/wider <task>` rewrites a task to use the methods of other fields, and names a red team that attacks the result.

Three evidence skills. They come from copyconstruct's post "How to effectively debug when you no longer understand the code".

- `signal-first-plan` runs before a feature is built. It lists every exit the feature's data leaves through, puts a countable signal on each, and checks the signals against main. Claude invokes it on its own when you ask for behaviour that ships to users or other systems.
- `debugging-by-constraints` runs on production bugs and review findings. It gathers facts first, picks a control, builds a hypotheses-by-fact matrix, and keeps the one hypothesis that fits every fact. Claude invokes it on its own, or you run `/debugging-by-constraints`.
- `/debug-retro` runs after a debug session. It counts each time you had to step in and turns each one into a lasting rule. It is the least exercised of the six.

## Install

Pick one of the three ways.

### Any agent, one skill at a time

The `skills` CLI from Vercel Labs (https://github.com/vercel-labs/skills) installs skills from a GitHub repo into the folder your agent reads. It needs Node.js 22.20 or later. Run it from your project:

```
npx skills add rajnandan1/sharper-skills
```

The CLI lists the six skills and the agents it finds on your machine, and you pick. Skills land in the current project. Add `-g` to install them for every project.

To skip the prompts, name the skills and the agents:

```
npx skills add rajnandan1/sharper-skills --list
npx skills add rajnandan1/sharper-skills --skill deeper -a claude-code
npx skills add rajnandan1/sharper-skills --skill debugging-by-constraints --skill debug-retro -a codex -a cursor -g
```

Later, `npx skills update` pulls new versions and `npx skills remove deeper` removes one.

In agents other than Claude Code, the three lenses take the task from your last message, because only Claude Code fills in the `<task>` argument.

### Claude Code, all six as a plugin

1. Run `/plugin marketplace add rajnandan1/sharper-skills`.
2. Run `/plugin install sharper-skills@sharper-skills`.

Installed as a plugin, each skill also answers to its prefixed name, such as `/sharper-skills:higher`.

### By hand

Copy the folders you want from `skills/` into the folder your agent reads: `~/.claude/skills/` for Claude Code, `~/.agents/skills/` for Codex, `~/.cursor/skills/` for Cursor.

## Where learned rules go

`debug-retro` writes what it learns about a codebase to `.claude/debug-layers.md` at that project's root. `debugging-by-constraints` and `signal-first-plan` read that file when it exists. The skill files stay unchanged, so a plugin update does not lose your rules. Rules about the method itself go to an issue or pull request in this repo.

`skills/debugging-by-constraints/LAYERS.md` lists the tools that reach each layer of facts. Its layer 1 table shows the author's stack as an example: Grafana, Prometheus, Railway, PostHog, ClickHouse, kubectl. Replace each with the tool that reaches the same fact in your stack.

## Sources

- Felix Rieseberg, "How to be more ambitious: A tutorial for humans with models": https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/
- copyconstruct, "How to effectively debug when you no longer understand the code": https://copyconstruct.medium.com/how-to-effectively-debug-when-you-no-longer-understand-the-code-bd3dcb2c5f7b

## License

MIT.
