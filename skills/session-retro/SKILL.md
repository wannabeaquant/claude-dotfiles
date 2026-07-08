---
name: session-retro
description: End-of-session learning capture - update MEMORY.md, ERRORS.md, and global memory with what happened, what worked, what failed, and corrections the user gave. Trigger when the user says session end, bye, done for today, wrap up, or at a natural long stopping point.
---

# Session Retro

The point: every session should leave the system smarter. Capture four things —
what happened, what failed, what the user corrected, and what patterns are
repeating.

## Steps

1. **Reconstruct the session.** `git log --oneline` since session start across
   touched repos, plus tasks completed vs abandoned. Flag any uncommitted or
   unpushed work to the user — don't silently leave it.

2. **Project MEMORY.md.** Append one Session Log line per self-contained unit
   of work (what + why). Add Decisions-table rows for anything that would cost
   >1hr to reverse or touches a public interface (with why + what was
   rejected). Refresh Next Session Priorities.

3. **Project ERRORS.md.** For anything this session that took 2+ attempts:
   what didn't work / what worked instead / note for next time. Be specific
   enough that next session can act on it without re-deriving.

4. **Corrections → global memory.** Scan the session for moments the user
   corrected course: rejected an approach, said "no, do X instead", reversed a
   decision, expressed annoyance at a behavior. For each, write or update a
   feedback-type memory file in the auto-memory directory (with **Why** and
   **How to apply**). These are the highest-value learning signal — do not skip.

5. **Wins.** If an approach worked first try and is reusable (a command
   sequence, a debugging path, a pattern), note it in MEMORY.md or propose a
   skill for it.

6. **Escalate repeating patterns.** If the same mistake now appears 2+ times
   (this ERRORS.md, another repo's ERRORS.md, or global memory), propose a
   concrete fix and let the user choose:
   - deterministic and checkable → a hook (in claude-dotfiles/hooks/)
   - a repeatable procedure → a skill (in claude-dotfiles/skills/)
   - a judgment-call rule → a CLAUDE.md line
   Never silently apply these — present the proposal in one short list.

7. **Agency workspace only:** also run the doc-sync skill (Doc Update Matrix).
