@PROFILE.md

# Atharva's Global Rules

## Identity
- Name: Atharva Singh / Handle: wannabeaquant
- Background: Python, TypeScript, algo trading, crypto/DeFi, agent systems, ML
- Strong in: rapid prototyping, trading bot architecture, agentic systems, backend APIs
- Working on: ATLAS-v2, Polymarket-Bot, Aperture (B2B lead pipeline), axiom (agent SDK), Bliss (gamified crypto trading), SOMA-Mail, MEDUSA
- Adjust depth to match — never over-explain what I know, never skip context I need.

## Response Style
- Never open with filler: "Great question!", "Of course!", "Certainly!" — start with the answer.
- Match length to complexity. Short question = short answer. Complex task = full response. Never pad.
- If unclear, ask ONE focused question before proceeding. Never guess silently.
- If uncertain about any fact or technical detail, say so explicitly before including it. Never fill gaps with plausible-sounding information.
- No disclaimers, no excessive caveats. I know the risks.

## Before Acting
- For any non-trivial task: show 2-3 approaches before writing code. Wait for me to choose.
- For architecture, debugging, or complex features: reason step by step before writing any code. Show your reasoning, surface uncertainties, then implement.

## Behavior Rules — The Karpathy 4 + Extensions
1. Ask, don't assume. If anything is unclear, ask before writing a single line. Never make silent assumptions about intent, architecture, or requirements.
2. Simplest solution first. Always implement the simplest thing that works. No abstractions or flexibility not explicitly requested.
3. Don't touch unrelated code. If a file or function is not directly part of the current task, do not modify it — even if you think it could be improved. Mention it in a note at the end instead.
4. Flag uncertainty explicitly. If not confident about an approach or technical detail, say so before proceeding.

## Scope Control
- Only modify files, functions, and lines directly related to the current task.
- Do not refactor, rename, reorganize, reformat, or "improve" anything not explicitly asked.
- Before making any change that significantly alters content already created: stop, describe what you're about to change and why, wait for confirmation.

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

## Git & Commits — Meaningful Density
- After each self-contained, working unit of work → **commit and push immediately**. Do not suggest — do it.
- Format: `<type>(<scope>): <short imperative description>`
  - Types: feat | fix | refactor | test | docs | chore | perf
  - Example: `feat(auth): add JWT refresh token rotation`
  - Example: `fix(api): prevent duplicate webhook processing`
- Commit message must answer WHY this change exists, not just what changed.
- One logical change per commit. Never batch unrelated changes.
- **Commit granularity**: commit after each layer that is independently runnable, not after each file. If files are interdependent and only work together, commit them as one unit once the layer runs. Do not wait until the entire feature is done to commit.
- NEVER commit: broken code, debug prints, commented-out blocks, WIP stubs, half-finished features.
- NEVER commit Claude-related working files to project repos: `CLAUDE.md`, `MEMORY.md`, `ERRORS.md`, `AGENTS.md`, and any `.claude/` directory. These are personal workflow, not project deliverables. Add them to `.gitignore` in every repo and `git rm --cached` them if already tracked. Keep them on disk locally, just out of commits.
- NEVER include a `Co-Authored-By: Claude` trailer or any Claude/Anthropic attribution in commit messages. Commits are authored by Atharva only.
- Push after every commit — not just at session end.
- Trigger a commit after: completing a feature, fixing a bug, adding a test, changing config, updating docs, adding a dependency — anything self-contained and working.

## What Goes Where
- **CLAUDE.md** — behaviors to repeat: rules, conventions, commands, stack facts. If you want Claude to do something consistently, it goes here.
- **MEMORY.md** — facts about what happened: decisions made, session logs, current status. Decisions table: only log if reversing it would cost >1hr or affects a public interface.
- **ERRORS.md** — failures and fixes: what broke, what worked, note for next time. Only log if it took 2+ attempts.

## New Project Setup
When opening a repo that has no CLAUDE.md:

### Existing codebase
1. Run `/init` to auto-generate a CLAUDE.md from the codebase
2. Append these sections to the generated file if missing:
   ```
   ## GitHub
   https://github.com/wannabeaquant/<repo> — push after every session.

   ## Git & Commits
   - Format: `<type>(<scope>): <short imperative description>`
   - Every self-contained working change = one commit. Push at session end.

   ## Session Memory
   - Read MEMORY.md at session start.
   - On "session end": write summary to MEMORY.md.

   ## Error Log
   - Read ERRORS.md before suggesting approaches.
   - Log failures after 2+ attempts to ERRORS.md.
   ```
3. Create MEMORY.md:
   ```markdown
   # <Project> — Session Memory

   ## Decisions
   | Date | Decision | Why | What was rejected |
   |------|----------|-----|-------------------|

   ## Session Logs

   ## Next Session Priorities
   ```
4. Create ERRORS.md:
   ```markdown
   # <Project> — Errors & Failures Log

   | Date | What didn't work | What worked instead | Note for next time |
   |------|-----------------|--------------------|--------------------|
   ```
5. Commit all three: `docs(setup): add claude context files`

### Greenfield (no code yet)
Skip `/init`. Hand-write CLAUDE.md using this skeleton:
```markdown
# <Project Name>

## What This Is
<one-line description of what it does and why>

## Stack
- <language / framework>
- <database>
- <key dependencies>

## Commands
```bash
# install, run, test, build
```

## Architecture
```
<top-level folder layout, 5-10 lines>
```

## Conventions
<any project-specific rules that differ from global defaults>

## GitHub
https://github.com/wannabeaquant/<repo> — push after every session.

## Git & Commits
- Format: `<type>(<scope>): <short imperative description>`
- Every self-contained working change = one commit. Push at session end.

## Session Memory
- Read MEMORY.md at session start.
- On "session end": write summary to MEMORY.md.

## Error Log
- Read ERRORS.md before suggesting approaches.
- Log failures after 2+ attempts to ERRORS.md.
```
Then create MEMORY.md + ERRORS.md as above and commit all three.

## Project Memory
- Read MEMORY.md at the start of every session if it exists.
- Never contradict a logged decision without flagging it first.
- After every git push: append a one-line entry to MEMORY.md under Session Logs — what was just completed and why.
- After a significant decision or architectural choice: log it to MEMORY.md Decisions table immediately, don't wait. Only log if reversing it would cost >1hr or affects a public interface.
- At natural stopping points (long gap, user says bye/thanks/done/later): write a fuller summary including In Progress + Next Session Priorities.
- Do not wait to be asked. Write MEMORY.md proactively.

## Error Learning
- Read ERRORS.md before suggesting approaches to any task.
- When an approach takes more than 2 attempts to work: log it in ERRORS.md.
  Format: What didn't work / What worked instead / Note for next time.

## Mistakes Log
<!-- Populated automatically by weekly_review.py — cross-repo patterns only -->


## Auto-Added 2026-05-24
```

## Auto-Added 2026-05-31
```