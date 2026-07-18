---
name: new-repo-setup
description: Initialize Codex project guidance and local continuity files for a repository. Use at the first commit in a new repo, when opening a repo without AGENTS.md, MEMORY.md, or ERRORS.md, or when the user asks to initialize or set up project context.
---

# New Repo Setup

Run this before the first commit rather than deferring project context.

1. Inspect the repository before writing guidance.
2. For an existing codebase, create a concise `AGENTS.md` covering purpose, stack, commands, architecture, conventions, verification, and repo-specific constraints. For greenfield work, write those sections from the chosen design and current files.
3. Add these operating sections when relevant:

   ```markdown
   ## Git and commits
   - Use `<type>(<scope>): <short imperative description>`.
   - Commit and push each self-contained, validated unit of work.

   ## Session memory
   - Read MEMORY.md and ERRORS.md before architecture or debugging work.
   - Use the session-retro skill at natural stopping points.
   ```

4. Create local `MEMORY.md`:

   ```markdown
   # <Project> - Session Memory

   ## Decisions
   | Date | Decision | Why | What was rejected |
   |------|----------|-----|-------------------|

   ## Session Logs

   ## Next Session Priorities
   ```

5. Create local `ERRORS.md`:

   ```markdown
   # <Project> - Errors and Failures Log

   | Date | What did not work | What worked instead | Note for next time |
   |------|-------------------|---------------------|--------------------|
   ```

6. Add these local workflow files to `.gitignore` unless the user explicitly wants shared team guidance:

   ```gitignore
   CLAUDE.md
   MEMORY.md
   ERRORS.md
   AGENTS.md
   PROFILE.md
   SESSION_NOTES.md
   .claude/
   .agents/
   ```

7. Do not commit the context files. Commit only the ignore change as `chore(setup): ignore local context files` after validation.
