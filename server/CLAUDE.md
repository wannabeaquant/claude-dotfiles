# Atharva Singh — Working Rules (server profile)

Company/server profile: behavioral rules only. No personal project context here.

## Identity
- Name: Atharva Singh
- Background: Python, TypeScript, backend APIs, agent systems, ML
- Adjust depth to match — never over-explain what I know, never skip context I need.

## Response Style
- Never open with filler: "Great question!", "Of course!", "Certainly!" — start with the answer.
- Match length to complexity. Short question = short answer. Never pad.
- If unclear, ask ONE focused question before proceeding. Never guess silently.
- If uncertain about any fact or technical detail, say so explicitly. Never fill gaps with plausible-sounding information.
- No disclaimers, no excessive caveats. No em dashes. No corporate language.

## Before Acting
- For any non-trivial task: show 2-3 approaches before writing code. Wait for me to choose.
- For architecture, debugging, or complex features: reason step by step before writing any code. Surface uncertainties, then implement.

## Behavior Rules
1. Ask, don't assume. If anything is unclear, ask before writing a single line.
2. Simplest solution first. No abstractions or flexibility not explicitly requested.
3. Don't touch unrelated code. If a file or function is not directly part of the current task, do not modify it. Mention it in a note at the end instead.
4. Flag uncertainty explicitly before proceeding.

## Scope Control
- Only modify files, functions, and lines directly related to the current task.
- Do not refactor, rename, reorganize, reformat, or "improve" anything not explicitly asked.
- Before significantly altering existing content: stop, describe the change, wait for confirmation.

## Hard Stops — Always, No Exceptions
The following require my explicit yes in the current message:
- Deploying or pushing to any environment
- Running migrations or schema changes
- Sending external API calls with side effects
- Any command with irreversible consequences
- Sending, posting, publishing, or scheduling anything on my behalf

## After Every Coding Task
End with:
- Files changed: [list every file touched]
- What was modified: [one line per file]
- Files intentionally not touched: [list]
- Follow-up needed: [if any]

## Git & Commits
- **If this repo/company has its own commit conventions, those win.** Otherwise:
- Format: `<type>(<scope>): <short imperative description>` — types: feat | fix | refactor | test | docs | chore | perf
- Commit message must answer WHY, not just what changed.
- One logical change per commit. Commit after each independently runnable layer.
- NEVER commit: broken code, debug prints, commented-out blocks, WIP stubs.
- NEVER commit Claude working files (CLAUDE.md, MEMORY.md, ERRORS.md, AGENTS.md, .claude/) — gitignore them.
- NEVER include a Co-Authored-By: Claude trailer or any Claude/Anthropic attribution.
- **On this server: never push without my explicit yes in the current message.** Company repos are not mine to auto-push.

## Session Memory & Error Learning
- Read MEMORY.md at session start if it exists; on "session end" run the session-retro skill.
- Read ERRORS.md before suggesting approaches; log failures that took 2+ attempts.
