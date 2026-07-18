---
name: session-retro
description: Detect natural work-session boundaries and capture learning in project memory and error logs without requiring the user to announce the end. Use when a substantial task or coherent batch is complete and handed off, the user acknowledges completion or shifts topics, no meaningful next action remains, continuing requires a later user decision, or the user explicitly says wrap up, done, bye, or end of session. Do not use mid-task, during active debugging, after a minor exchange, or while promised work remains.
---

# Session Retro

Codex owns boundary detection. Never require the user to provide a magic phrase.

## Judge the boundary

Treat the current point as a natural stop when one or more strong signals apply and no negative signal applies.

Strong signals:

- A substantial requested task or coherent batch is complete, verified, committed or handed off, and no promised action remains.
- The user acknowledges the result with language such as "thanks", "perfect", "looks good", or "that works".
- The user shifts to an unrelated topic after completed work.
- The only next step requires a later decision, credential, external event, or new authorization from the user.
- The conversation has reached a clean milestone where a fresh task could resume from written state without losing context.

Negative signals:

- Implementation, verification, commit, push, or another promised step is still running or incomplete.
- Debugging is active, a test is failing, or the user is answering a clarification needed to continue.
- The exchange was only a small question with no durable project state.
- The user asks for status and expects work to continue.

When signals are mixed, continue the task. Do not interrupt merely to ask whether the session is ending.

## Capture the session

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
8. Perform the retro proactively and quietly. In the normal handoff, mention only actual memory/error updates, promotions needing a decision, and remaining uncommitted or unpushed work. Do not add ceremony when nothing durable needed recording.
