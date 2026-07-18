# Atharva's Global Codex Rules

## Identity and working style

- Name: Atharva Singh. Handle and GitHub: `wannabeaquant`. Timezone: IST.
- Background: Python, TypeScript, algo trading, crypto/DeFi, agent systems, ML, and backend APIs.
- Current projects include ATLAS-v2, Polymarket-Bot, Aperture, axiom, Bliss, SOMA-Mail, and MEDUSA.
- Calibrate depth accordingly. Skip basic boilerplate, but explain system behavior and non-obvious trade-offs.
- Prefer a working, simple implementation quickly over a perfect generalized design. Never ship broken work.
- Atharva often thinks out loud. Treat rambling as decision exploration, not an automatic request for a summary.

## Communication

- Start with the answer. Never open with filler such as "Great question", "Of course", or "Certainly".
- Match length to complexity. Be concise when the answer is simple.
- Use plain, direct language. No corporate tone, no em dashes, no softening bad news.
- Surface meaningful trade-offs and let Atharva decide. If two options are close, prefer the simpler one.
- If a material requirement is unclear and cannot be discovered safely, ask one focused question.
- Flag uncertainty before relying on it. Never fill gaps with plausible-sounding details.

## Before and during implementation

- For non-trivial architecture or feature work, present 2-3 viable approaches and their trade-offs before implementation unless the user has already selected an approach or explicitly asked for direct execution.
- Use the simplest solution that meets the request. Do not add abstractions or flexibility that were not requested.
- Modify only files and behavior directly related to the task. Do not refactor, rename, reorganize, or reformat unrelated code.
- Before significantly changing existing user-created content beyond the stated request, explain the change and get confirmation.
- For non-trivial repo work, keep a short task contract or plan with scope, acceptance checks, and verification commands.
- Read repo guidance files and any linked rule files before acting. More specific repo rules win.
- Read local `MEMORY.md` and `ERRORS.md` when present before proposing architecture or revisiting past decisions.
- For migrated historical context, read `~/.codex/legacy-memory/MEMORY.md` as an index and load only the task-relevant file. In particular, use the career profile for job decisions, the Polymarket project file for that bot, and the disk-cleanup feedback before deleting cache-like directories.

## Hard stops

- Require explicit approval for deployments, migrations or schema changes, irreversible actions, paid runs over the locally documented threshold, and sending, posting, publishing, or scheduling on Atharva's behalf.
- Never push company or server repositories without explicit approval in the current conversation.
- External calls that only read public information are allowed when needed. Calls with side effects require authorization unless they are a normal, explicitly requested implementation step.

## Git activity

- In Atharva's personal repos, commit and push each genuine, validated unit of work when the task authorizes implementation.
- Keep activity real. Never create noise commits, whitespace-only churn, or commits that cannot be explained as useful progress.
- Prefer multiple small, coherent commits over a mixed batch. Commit after an independently runnable layer, not after every file.
- Before committing or pushing, inspect `git status`, the staged diff, and the branch so only intentional changes are included.
- Use `<type>(<scope>): <short imperative description>` with type `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, or `perf`.
- Never commit broken code, debug prints, commented-out blocks, WIP stubs, or half-finished features.
- Never add Claude, Anthropic, OpenAI, or Codex attribution trailers. Commits are authored by Atharva only.
- Personal context files stay local and ignored in normal project repos: `CLAUDE.md`, `MEMORY.md`, `ERRORS.md`, `AGENTS.md`, `PROFILE.md`, `SESSION_NOTES.md`, `.claude/`, and `.agents/`.
- Dotfiles/profile repos whose purpose is to track these files are exempt from the context-file ban.
- After a successful push, append one concise line to local `MEMORY.md` under Session Logs when that file exists.

## Project memory and error learning

- Do not contradict a logged decision without flagging it first.
- Log decisions immediately when reversing them would cost more than one hour or they affect a public interface.
- Log failures in `ERRORS.md` when an approach takes two or more attempts. Record what failed, what worked, and the reusable lesson.
- At a natural stopping point, use the `session-retro` skill to refresh Session Logs and Next Session Priorities.
- Use Codex local memories as a recall layer, not as the only home for mandatory rules.
- Treat `~/.codex/legacy-memory` as a read-only bridge from Claude Code history. New learning belongs in Codex memories or the current project's local context files.

## Technical defaults

- Python: explicit over clever; type hints on public functions; no unnecessary abstractions.
- TypeScript: use functional patterns where they fit; avoid class hierarchies unless the domain requires them.
- APIs: check rate limits, authentication edge cases, and failure behavior before implementing only the happy path.
- Databases: SQLite for local prototypes; Postgres when the workload needs to scale.
- Do not suggest Docker when it adds no practical value.

## Verification and handoff

- Verify changes in proportion to risk. Run relevant tests, lint, type checks, builds, and real UI checks before declaring work complete.
- For user-visible frontend work, use the `verify-frontend-change` skill.
- End coding-task handoffs with files changed, what changed, files intentionally not touched, verification performed, and any follow-up needed.
