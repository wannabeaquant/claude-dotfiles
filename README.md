# Claude Code and Codex dotfiles

Source of truth for Atharva's Claude Code and Codex configuration. Edit here,
run the matching installer, verify, commit, and push. Do not edit installed
copies directly because installers overwrite them.

## Layout

```text
home/                       Full personal Claude Code profile
server/                     Slim company-safe Claude Code profile
hooks/                      Claude Code PreToolUse commit guard
skills/                     Claude Code workflow skills
codex/home/AGENTS.md        Full personal Codex guidance
codex/server/AGENTS.md      Slim company-safe Codex guidance
codex/skills/               Codex-native workflow skills
codex/git-hooks/            Tool-independent Git commit policy
review/                     Weekly pattern review and scope config
settings.windows.json       Windows Claude Code settings
install.ps1                 Windows Claude Code installer
install.sh                  Server Claude Code installer
install-codex.ps1           Windows Codex installer
install-codex.sh            Server Codex installer
tests/                      Git-guard tests
```

## Install

Windows personal machine:

```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
powershell -ExecutionPolicy Bypass -File install-codex.ps1
```

Company server after cloning the repo:

```bash
bash ~/claude-dotfiles/install.sh
bash ~/claude-dotfiles/install-codex.sh
```

The Codex installer:

- installs global guidance to `~/.codex/AGENTS.md`;
- installs global skills to `~/.agents/skills`;
- enables Codex local memories;
- copies historical Claude memory into `~/.codex/legacy-memory` as a read-only
  continuity bridge while Codex builds its own memories;
- installs global Git hooks through `core.hooksPath`, covering commits made by
  humans or any coding tool while preserving repo-local hooks;
- backs up existing Codex guidance, config, skills, and hook-path settings;
- leaves `~/.claude` and the Claude scheduled review untouched.

## Weekly review

`WeeklyClaudeReview` runs Sundays at 23:00 through Windows Task Scheduler. Its
scope is defined in `review/review_config.json`. Run it manually with:

```powershell
python "$env:USERPROFILE\.claude\weekly_review.py" --dry-run
```

The Codex installer does not replace or reschedule this task automatically.
The existing job invokes the Claude CLI and pushes the profile report, so
changing its reviewer backend is an explicit migration choice.

## Learning loop

1. Project decisions and failures stay in local `MEMORY.md` and `ERRORS.md`.
2. `session-retro` captures end-of-session learning and proposes promotions.
3. The weekly review analyzes real Git activity and evidence from local docs.
4. Repeated deterministic failures become hooks or tests; repeatable procedures
   become skills; judgment calls stay in global or repo guidance.
