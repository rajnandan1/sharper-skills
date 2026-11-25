# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Static HTML and CSS in `site/` in the `rajnandan1/sharper-skills` repo, with no build step. GitHub Pages serves the site from `main`. A subdomain, not yet chosen, will point at the site later through a CNAME record. The user chose this stack and host on 2026-11-25.

## Users

Developers who already use a coding agent: Claude Code, Codex, Cursor, OpenCode, Gemini CLI or GitHub Copilot. They arrive from a link, such as the README, a release or a post. They want to know which skill fits their problem, and they should leave with an install command copied.

## Product Purpose

sharper-skills is a set of eight open-source skills for coding agents. Each skill is a folder with a `SKILL.md` file: written instructions that the agent loads and follows. Seven skills shape what the agent does around the task (see Capabilities for each one). One skill, `/leonardo`, does open-ended work itself, such as a name, a concept, copy or a design. Success means a visitor installs one or more skills.

## Positioning

A line of instruction enters a `SKILL.md` only when a real session transcript or a behavioural run (a scripted run of the skill on a test task) shows the outcome the line would have changed. A claim that fails that bar is recorded as rejected, with its reason, in the release notes. Each skill names the post or research it comes from, and the GitHub release notes publish the audits and test runs, including losses: in the v0.12.0 blind test, three model judges each preferred the plain agent's answer (the agent with no skill loaded) over `/leonardo`'s when a naming task was re-run on the final skill text.

## Operating Context

- Install with the Vercel Labs `skills` CLI: `npx skills add rajnandan1/sharper-skills` (Node.js 22.20 or later).
- Install in Claude Code as a plugin: `/plugin marketplace add rajnandan1/sharper-skills`, then `/plugin install sharper-skills@sharper-skills`.
- Install by hand by copying skill folders into `~/.claude/skills/`, `~/.agents/skills/` or `~/.cursor/skills/`.
- Start a skill by typing `/name` (Codex uses `$name`). `signal-first-plan` and `debugging-by-constraints` also start on their own.

## Capabilities and Constraints

- `/higher` rewrites a task to ask for the outcome one level up.
- `/deeper` rewrites a task to use the inputs, methods and checks a top professional would use.
- `/wider` rewrites a task to use the methods of other fields, plus a red team that attacks the result.
- The three above are prompt lenses: each hands the rewritten prompt back, and the user replies `go` to run it.
- `signal-first-plan` runs before a feature is built: it puts a countable signal on every exit the feature's data leaves through.
- `debugging-by-constraints` runs on production bugs and review findings: facts first, a control case, and a matrix of hypotheses against facts.
- `/debug-retro` runs after a debug session and turns each time the user had to step in into a lasting rule.
- `/leonardo` does an open-ended task and tries to beat the plain agent's answer in a blind pick.
- `/defend` writes an HTML report on what a session decided and changed, then quizzes the user and grades the answers.
- MIT license. Repo: https://github.com/rajnandan1/sharper-skills. Plugin version 0.12.0.
- The README is the source of truth for skill descriptions; the site must not contradict it.

## Brand Commitments

- Name: `sharper-skills`, lowercase, with the hyphen.
- Logo: the `>` prompt sign drawn as two blades that taper to one point; the wordmark is JetBrains Mono Bold converted to outlines, with a small blade for the hyphen. Files and rules in `brand/` and `brand/GUIDELINES.md` (clear space, minimum sizes, the do-not list).
- Colours: Ink `#141414`, Paper `#F4F2EC`, Signal `#F04E23`, with the pairings in `brand/GUIDELINES.md`. Signal on Paper only at 48 px and up.
- Type next to the logo: JetBrains Mono for code and labels, the platform's default sans-serif for other text.
- Web icons and manifest: `brand/web/`.
- Voice: plain English in the style of Simplified Technical English, as in the README. No hype.

## Evidence on Hand

- `README.md` text, including its Sources list, and the eight `SKILL.md` files.
- GitHub release notes: v0.12.0 (a blind test where three model judges compared `/leonardo` with the plain agent on three tasks: it won two, and lost the naming task when it was re-run on the final skill text) and v0.5.0 (six outside sources checked against the skills: three lines added, the rest rejected with reasons).
- Brand slides: `brand/presentation/slide-01.png` to `slide-05.png`.
- Absent, never to be invented: testimonials, user or install counts, GitHub star counts, company logos, benchmarks beyond the published runs.

## Product Principles

1. Evidence decides what goes into a skill, and the losses get published with the wins.
2. Seven of the eight skills make the agent more exact around the task instead of doing more of it. The eighth, `/leonardo`, does the task and is tested blind against the agent alone.
3. Plain words: a reader should understand a skill on one read.
4. Skills work in any agent that reads `SKILL.md`.
