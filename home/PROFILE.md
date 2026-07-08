# Atharva Singh — User Profile

## Who I Am
- Handle: wannabeaquant | GitHub: github.com/wannabeaquant
- Timezone: IST (Asia/Calcutta, UTC+5:30)
- Background: Python, TypeScript, algo trading, crypto/DeFi, agent systems, ML
- Currently: CS student, building real products alongside studies

## How I Work
- Rapid prototyper — I'd rather have something working in 2 hours than a perfect plan in 2 days
- I run multiple projects in parallel — context-switch often, so project-level MEMORY.md matters a lot
- I prefer to understand the system, not just copy-paste solutions
- I think out loud — if I'm rambling it means I'm working through a decision, not asking for a summary
- I don't need hand-holding on basics. Skip boilerplate explanations.

## Communication Preferences
- Short > long. If it fits in 2 lines, don't write 6.
- Show me the trade-offs, then let me decide. Don't decide for me silently.
- If something will break, tell me before doing it.
- Don't soften bad news. Just say it.
- No em dashes. No corporate language. Talk like a person.

## Technical Defaults
- Python: prefer explicit over clever. Type hints on public functions. No unnecessary abstractions.
- TypeScript: functional where it fits, avoid class hierarchies unless the domain demands it
- APIs: always check for rate limits and auth gotchas before writing the happy path
- DBs: SQLite for local/prototype, Postgres for anything that needs to scale
- Never suggest Docker for something that doesn't need it

## Decision-Making Style
- Ship first, polish later — but never ship broken
- I'll take on tech debt consciously if it gets me to a working demo faster
- I care about contribution graph density — commits should be real and frequent, not padded
- If two options are close, I'll pick the simpler one

## Current Focus (as of May 2026)
- ATLAS-v2: deterministic paper trading scaffold
- Polymarket-Bot: live alpha strategies
- Aperture: B2B lead pipeline
- axiom: local-first agent SDK
- Bliss: gamified crypto trading app
- SOMA-Mail: email agent

## Auto-Updated
<!-- weekly_review.py appends observed patterns here every Sunday -->

### 2026-05-24
- ```
- Commit format discipline holds on backend/logic work but degrades during fast visual/UI iteration sprints. Flag this before starting any frontend-heavy session.
- Builds greenfield projects in single focused sessions — full implementation + one correctness pass. Does not spread greenfield work across multiple sessions.
- Self-correction loop is active: catches own process violations (batched commits, etc.) and logs them to ERRORS.md in the same session.
- ```

### 2026-05-31
- ```
- Format discipline degrades not just during frontend sprints but also during doc/polish/eval sprints — `(scope)` gets dropped from docs commits and ad-hoc types like `eval` appear. Flag this at the start of any session that is primarily docs or evaluation work, not just UI work. # confirmed 2026-05-31 in pr-review-context
- New repos get built in a single session (consistent with greenfield pattern) but CLAUDE.md setup is deferred or skipped. This has now occurred 3+ times. The build instinct is strong; the context-file instinct is weak. Auto-trigger CLAUDE.md setup check at first commit of any new repo.
- ```
