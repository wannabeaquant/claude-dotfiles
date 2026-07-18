---
name: session-retro
description: Capture end-of-session learning in project memory and error logs, assess corrections and reusable wins, and propose promotion into rules, hooks, or skills. Use when the user says session end, wrap up, done for today, bye, or at a natural long stopping point.
---

# Session Retro

1. Reconstruct the session from the conversation, `git status`, and relevant `git log`. Identify completed, abandoned, uncommitted, and unpushed work.
2. Append one concise Session Log entry per completed unit to local `MEMORY.md`. Add decision rows only for choices that affect a public interface or would cost more than one hour to reverse. Refresh Next Session Priorities.
3. Add `ERRORS.md` entries for failures that took two or more attempts. Record what failed, what worked, and the next-time lesson.
4. Identify user corrections, rejected approaches, reversals, and expressed friction. Codex local memory generation handles cross-chat recall when enabled; keep mandatory behavior in `AGENTS.md`, not only in memory.
5. Record reusable first-try wins in `MEMORY.md` or propose a skill when the procedure is broadly repeatable.
6. When a mistake appears at least twice, propose one concrete promotion and wait for the user to choose:
   - deterministic and checkable: Git hook, Codex lifecycle hook, linter, or test
   - repeatable procedure: skill
   - judgment call: `AGENTS.md` rule
7. In `C:\CS\Agency`, also use the `doc-sync` skill.
8. Report changes made to memory/error files and call out any remaining uncommitted or unpushed work.
