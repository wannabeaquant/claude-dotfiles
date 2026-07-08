---
name: new-repo-setup
description: Set up Claude context files (CLAUDE.md, MEMORY.md, ERRORS.md) in a repo that has none. Trigger at the FIRST commit in any new repo, when opening a repo without a CLAUDE.md, or when the user asks to set up / initialize a project.
---

# New Repo Setup

The build instinct is strong, the context-file instinct is weak — this setup has
been skipped 3+ times historically. Run this BEFORE the first commit lands, not
"later".

## Steps

1. **Existing codebase**: run `/init` to generate CLAUDE.md from the code, then
   append the standard sections below if missing.
   **Greenfield**: hand-write CLAUDE.md with: What This Is (one line), Stack,
   Commands (install/run/test), Architecture (5-10 line folder layout),
   Conventions.

2. Append to CLAUDE.md in both cases:

   ```markdown
   ## GitHub
   https://github.com/wannabeaquant/<repo> — push after every session.

   ## Git & Commits
   - Format: `<type>(<scope>): <short imperative description>`
   - Every self-contained working change = one commit. Push after every commit.

   ## Session Memory
   - Read MEMORY.md at session start.
   - On "session end": run the session-retro skill.

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

5. Add to `.gitignore`:

   ```
   CLAUDE.md
   MEMORY.md
   ERRORS.md
   AGENTS.md
   SESSION_NOTES.md
   .claude/
   ```

6. **Do NOT commit any of these files.** They stay local. This supersedes any
   older instruction to commit them — the commit_guard hook will block it
   anyway. Commit the `.gitignore` change itself as
   `chore(setup): ignore local context files`.
