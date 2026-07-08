# claude-dotfiles

Source of truth for my Claude Code configuration. Edit here, run the installer,
commit, push. Never edit `~/.claude` directly — it gets overwritten on install.

## Layout

```
home/                  Full personal profile (Windows machine)
  CLAUDE.md            Global rules (imports PROFILE.md)
  PROFILE.md           Who I am, how I work, auto-updated observations
server/                Slim company-safe profile (SSH servers)
  CLAUDE.md            Behavioral rules only, no personal project context
hooks/
  commit_guard.py      PreToolUse: blocks bad commit formats, Claude attribution,
                       and personal context files in project repos
skills/
  new-repo-setup/      Context-file setup at first commit of any new repo
  verify-frontend-change/  Browser-level verification before "done"
  session-retro/       End-of-session learning capture (MEMORY/ERRORS/global memory)
review/
  weekly_review.py     Weekly Claude-powered pattern review (Windows scheduled task)
  review_config.json   Which workspaces/repos the review covers
settings.windows.json  ~/.claude/settings.json for the Windows box (hooks wired)
install.ps1            Windows installer
install.sh             Linux/macOS server installer (server profile)
```

## Install

**Windows (this machine):**
```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

**SSH server (company box):**
```bash
git clone https://github.com/wannabeaquant/claude-dotfiles ~/claude-dotfiles
bash ~/claude-dotfiles/install.sh
```
Then authenticate Claude Code on the server once (`claude` → login) if not
already done via the VS Code extension.

## Weekly review

Runs Sundays 23:00 via Windows Task Scheduler (task `WeeklyClaudeReview`,
registered by `~/.claude/register_weekly_review.bat`). Scope is controlled by
`review/review_config.json` — add/remove workspaces or repos there and rerun
`install.ps1`. Manual run: `python ~/.claude/weekly_review.py` (`--dry-run` to
preview without calling Claude).

## The learning loop

1. **During a session**: corrections and decisions land in auto-memory,
   project MEMORY.md, ERRORS.md (via global rules + session-retro skill).
2. **Session end**: `session-retro` consolidates — session log, errors,
   feedback memories, and proposes rules/skills/hooks when a mistake repeats.
3. **Weekly**: `weekly_review.py` reads everything across active repos,
   assesses what Claude got right/wrong, auto-appends evidence-based
   observations to PROFILE.md / CLAUDE.md, and proposes (report-only) new
   skills and hooks.
4. **Deterministic failures get promoted out of prose**: recurring mistakes
   become hooks or skills in this repo, so enforcement stops depending on the
   model remembering a rule.
