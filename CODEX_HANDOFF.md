# Codex Handoff — Atharva's Claude Code Setup

Written 2026-07-19. Atharva is moving to Codex for ~1 month starting 2026-07-19/20.
This file is the complete state of his Claude Code configuration so Codex can pick
up the same rules, enforcement, and workflow without him re-explaining anything.
Read this fully before touching any of his repos.

Everything below is the actual current state, not aspirational — file paths, exact
file contents, and what is/isn't built yet are all as of this date.

---

## 1. Why this setup exists

Atharva runs many parallel projects (agency client work, a trading bot, personal
tools) and was previously enforcing all conventions (commit format, what never gets
committed, doc-update discipline) as prose instructions only. Prose degrades under
load — it was empirically observed to degrade specifically during fast UI/demo
sprints and docs/eval sprints (format discipline drops, ad-hoc types appear). The
fix applied: move anything deterministic and checkable out of prose and into code
(hooks), move anything procedural-but-repeatable into skills, and keep only actual
judgment calls as prose rules. A weekly review process closes the loop by reading
real git activity and proposing which prose rules should be promoted to hooks/skills
next.

The four-layer learning loop in place:
1. **In-session**: corrections and decisions get captured into memory as they happen.
2. **Session end**: a `session-retro` skill reconstructs the session, updates
   project MEMORY.md/ERRORS.md, saves corrections as global feedback memory, and
   proposes promoting repeat mistakes to a hook/skill.
3. **Weekly** (Sundays 23:00, Windows Task Scheduler): a script reads git activity
   across active repos + their CLAUDE.md/MEMORY.md/ERRORS.md, has Claude assess
   what it got right/wrong, and auto-appends evidence-based observations to
   PROFILE.md/CLAUDE.md.
4. **Promotion**: recurring deterministic failures get turned into hooks/skills in
   this repo so enforcement stops depending on the model remembering a rule.

---

## 2. Where everything lives

**Source of truth (edit here, never edit `~/.claude` directly):**
`C:\CS\claude-dotfiles` — private repo, `github.com/wannabeaquant/claude-dotfiles`
(gh CLI is authenticated as `wannabeaquant`, token scopes: gist, read:org, repo,
workflow). 2 commits on `master` as of writing.

```
claude-dotfiles/
  home/CLAUDE.md            full personal global rules (Windows machine)
  home/PROFILE.md           who Atharva is, how he works, auto-updated observations
  server/CLAUDE.md          slim, company-safe profile (no personal project context)
  hooks/commit_guard.py     PreToolUse hook — commit format + attribution + banned-file guard
  skills/new-repo-setup/SKILL.md
  skills/verify-frontend-change/SKILL.md
  skills/session-retro/SKILL.md
  review/weekly_review.py   weekly pattern-review script (v2)
  review/review_config.json  which workspaces/repos the review covers
  settings.windows.json     ~/.claude/settings.json for the Windows box (hooks wired in)
  install.ps1               Windows installer (backs up old config, copies everything in)
  install.sh                Linux/macOS server installer (slim profile)
  .gitattributes            forces LF endings on .sh/.py so install.sh runs on Linux
  README.md                 short version of this same explanation
```

**Installed locations (Windows machine, already live):**
`C:\Users\athar\.claude\CLAUDE.md`, `PROFILE.md`, `settings.json`, `hooks\commit_guard.py`,
`skills\*`, `weekly_review.py`, `review_config.json`. Previous config backed up at
`C:\Users\athar\.claude\backups\dotfiles-20260708-143001\`.

**Not yet installed:** the SSH/company server. Atharva has been given the one-liner
(`git clone ... ~/claude-dotfiles && bash ~/claude-dotfiles/install.sh`) but as of
this handoff it has not been confirmed run on the actual server — only unit-tested
locally.

**Agency-local (NOT in dotfiles — lives with the Agency workspace itself):**
`C:\CS\Agency\.claude\skills\doc-sync\SKILL.md`
`C:\CS\Agency\.claude\skills\apify-run\SKILL.md`
These are specific to the Agency's Doc Update Matrix and paid-scraping spend
discipline; they don't belong in the portable dotfiles repo because they encode
business-specific process, not general Claude config.

---

## 3. Global rules — `home/CLAUDE.md` (full content, installed as `~/.claude/CLAUDE.md`)

```markdown
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
[KNOWN INCONSISTENCY — see §9 "Open items". This section's original text still says
to commit CLAUDE.md/MEMORY.md/ERRORS.md to the new repo; that directly contradicts
the "Git & Commits" section above (never commit them) and the commit_guard hook now
blocks it outright. The `new-repo-setup` skill (§5) has already been corrected to
follow the never-commit rule. The raw text of this section in the live file has NOT
been edited yet — treat "Git & Commits" + the `new-repo-setup` skill as authoritative,
not this section, until Atharva confirms the cleanup.]

When opening a repo that has no CLAUDE.md: see the `new-repo-setup` skill instead of
the (stale) inline steps that used to live here.

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
```

*(The full original file also has an empty "Mistakes Log" placeholder comment and
two dated "Auto-Added" headers from the weekly review that are currently empty —
harmless, left as-is.)*

---

## 4. `home/PROFILE.md` (full content, installed as `~/.claude/PROFILE.md`)

```markdown
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
### 2026-05-24
- Commit format discipline holds on backend/logic work but degrades during fast visual/UI iteration sprints. Flag this before starting any frontend-heavy session.
- Builds greenfield projects in single focused sessions — full implementation + one correctness pass. Does not spread greenfield work across multiple sessions.
- Self-correction loop is active: catches own process violations (batched commits, etc.) and logs them to ERRORS.md in the same session.

### 2026-05-31
- Format discipline degrades not just during frontend sprints but also during doc/polish/eval sprints — `(scope)` gets dropped from docs commits and ad-hoc types like `eval` appear. Flag this at the start of any session that is primarily docs or evaluation work, not just UI work. # confirmed 2026-05-31 in pr-review-context
- New repos get built in a single session (consistent with greenfield pattern) but CLAUDE.md setup is deferred or skipped. This has now occurred 3+ times. The build instinct is strong; the context-file instinct is weak. Auto-trigger CLAUDE.md setup check at first commit of any new repo.
```

**Note on the last line above:** that exact gap (`new-repo-setup` not auto-triggering)
is what the `new-repo-setup` skill in this repo was built to close. As of this
handoff it exists as a skill but its actual trigger reliability across sessions
hasn't been re-measured by a weekly review yet.

Since 2026-07-08 this file is also updated automatically by `weekly_review.py`
(§7) under the same `## Auto-Updated` header — check for new dated sub-sections
appended after this handoff was written.

---

## 5. Server profile — `server/CLAUDE.md` (installed on SSH/company boxes only)

Deliberately slim: behavioral/response-style rules only, **no personal project
context, no Agency/business info**. This is what `install.sh` puts on the company
server so nothing personal leaks there.

```markdown
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
```

---

## 6. The commit guard hook — `hooks/commit_guard.py`

**Mechanism:** Claude Code `PreToolUse` hook, matcher `Bash|PowerShell`. Runs before
every shell command Claude executes; receives JSON on stdin
(`{tool_name, tool_input: {command}, cwd, ...}`), exits 2 with a stderr message to
**block** the command (Claude sees the stderr and can retry differently), exits 0
to allow it. Wired in `settings.windows.json`:

```json
"hooks": {
  "PreToolUse": [
    {
      "matcher": "Bash|PowerShell",
      "hooks": [
        { "type": "command", "command": "C:\\Users\\athar\\AppData\\Local\\Programs\\Python\\Python313\\python.exe C:\\Users\\athar\\.claude\\hooks\\commit_guard.py" }
      ]
    }
  ]
}
```

**What it blocks** (only fires if the command contains both `git` and `commit`):
1. Commit subjects not matching `<type>(<scope>): <description>` where type is one
   of `feat|fix|refactor|test|docs|chore|perf`. Exempts `merge`/`revert`/`fixup!`/
   `squash!`/`initial commit` subjects.
2. Claude/Anthropic attribution anywhere in the command (`Co-Authored-By: ...Claude`
   or `Generated with...Claude`, case-insensitive).
3. Commits touching `CLAUDE.md`, `MEMORY.md`, `ERRORS.md`, `AGENTS.md`, `PROFILE.md`,
   or any `.claude/` path — checked two ways: (a) `git diff --cached --name-only` in
   the repo, and (b) a regex scan of the command text itself, to catch
   `git add X && git commit` in one shell call before X is staged.
4. **Exempt repos** (by top-level folder name, case-insensitive):
   `claude-dotfiles`, `dotfiles`, `wannabeaquant` — these repos exist specifically to
   track these files.
5. **Fails open** on any unexpected exception (`sys.exit(0)`) — a broken hook must
   never brick the workflow.

It extracts commit messages from `-m "..."` / `-m '...'`, bash heredocs
(`$(cat <<'EOF' ... EOF)`), and PowerShell here-strings (`@'...'@`) to handle every
message-passing style used in this session.

**Full source** (146 lines, copy verbatim if porting the check itself rather than
the Claude-hook wrapper):

```python
#!/usr/bin/env python3
"""PreToolUse hook: guards git commits before they run.

Blocks:
  1. Commit subjects that don't follow <type>(<scope>): <description>
  2. Claude/Anthropic attribution (Co-Authored-By, "Generated with Claude")
  3. Commits touching personal working files (CLAUDE.md, MEMORY.md, ERRORS.md,
     AGENTS.md, PROFILE.md, .claude/) in project repos

Fail-open by design: any unexpected error exits 0 so a broken hook never
bricks the workflow. Exit 2 = block; stderr is fed back to Claude.
"""
import json
import re
import subprocess
import sys

TYPES = "feat|fix|refactor|test|docs|chore|perf"
SUBJECT_RE = re.compile(rf"^({TYPES})\([^)]+\): \S")
EXEMPT_SUBJECT_RE = re.compile(r"^(merge|revert|fixup!|squash!|initial commit)", re.I)
ATTRIBUTION_RE = re.compile(
    r"co-authored-by\s*:[^\n]*(claude|anthropic)|generated with[^\n]*claude", re.I
)
BANNED_FILES = {"claude.md", "memory.md", "errors.md", "agents.md", "profile.md"}
BANNED_DIR = ".claude"
# Repos where committing these files is the whole point
EXEMPT_REPOS = {"claude-dotfiles", "dotfiles", "wannabeaquant"}


def extract_messages(command):
    """Best-effort extraction of commit message contents from a shell command."""
    msgs = []
    # -m "..." (double-quoted, allows escapes) and -m '...' (single-quoted)
    for m in re.finditer(r"""-m\s+("((?:[^"\\]|\\.)*)"|'([^']*)')""", command):
        msg = m.group(2) if m.group(2) is not None else m.group(3)
        if msg and msg.lstrip().startswith("$("):
            continue  # command substitution wrapper; heredoc extractor gets the content
        msgs.append(msg)
    # bash heredoc: $(cat <<'EOF' ... EOF)
    for m in re.finditer(r"<<\s*'?EOF'?\r?\n(.*?)\r?\nEOF", command, re.S):
        msgs.append(m.group(1))
    # PowerShell here-strings: @' ... '@ / @" ... "@
    for m in re.finditer(r"@['\"]\r?\n(.*?)\r?\n['\"]@", command, re.S):
        msgs.append(m.group(1))
    return [m for m in msgs if m and m.strip()]


def repo_name(cwd):
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd or None, capture_output=True, text=True, timeout=10,
        )
        top = r.stdout.strip()
        if not top:
            return ""
        return top.replace("\\", "/").rstrip("/").split("/")[-1].lower()
    except Exception:
        return ""


def staged_files(cwd):
    try:
        r = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            cwd=cwd or None, capture_output=True, text=True, timeout=10,
        )
        return [l.strip() for l in r.stdout.splitlines() if l.strip()]
    except Exception:
        return []


def banned_hits(command, cwd):
    hits = set()
    for path in staged_files(cwd):
        norm = path.replace("\\", "/").lower()
        base = norm.split("/")[-1]
        if base in BANNED_FILES or norm.startswith(BANNED_DIR + "/") or "/" + BANNED_DIR + "/" in norm:
            hits.add(path)
    # scan the command itself — covers `git add X && git commit` in one call,
    # where X is not yet staged when this hook fires
    lowered = command.lower()
    for f in BANNED_FILES:
        if re.search(r"\bgit\s+(add|commit)\b[^\n|;&]*" + re.escape(f), lowered):
            hits.add(f.upper().replace(".MD", ".md"))
    if re.search(r"\bgit\s+add\b[^\n|;&]*\.claude\b", lowered):
        hits.add(".claude/")
    return sorted(hits)


def main():
    data = json.load(sys.stdin)
    if data.get("tool_name") not in ("Bash", "PowerShell"):
        return 0
    command = (data.get("tool_input") or {}).get("command") or ""
    if not re.search(r"\bgit\b", command) or not re.search(r"\bcommit\b", command):
        return 0
    cwd = data.get("cwd") or ""

    problems = []

    if ATTRIBUTION_RE.search(command):
        problems.append(
            "Commit contains Claude/Anthropic attribution. Remove the "
            "Co-Authored-By / 'Generated with Claude' trailer — commits are "
            "authored by Atharva only."
        )

    for msg in extract_messages(command):
        subject = msg.strip().splitlines()[0].strip()
        if not subject:
            continue
        if EXEMPT_SUBJECT_RE.match(subject):
            continue
        if not SUBJECT_RE.match(subject):
            problems.append(
                'Commit subject "%s" does not match <type>(<scope>): <description> '
                "with type one of: %s. "
                "Example: feat(auth): add JWT refresh token rotation"
                % (subject, TYPES.replace("|", ", "))
            )

    if repo_name(cwd) not in EXEMPT_REPOS:
        hits = banned_hits(command, cwd)
        if hits:
            problems.append(
                "This commit includes personal working files that must never be "
                "committed to project repos: %s. Unstage them "
                "(git restore --staged <file>) and add them to .gitignore instead."
                % ", ".join(hits)
            )

    if problems:
        print(
            "COMMIT BLOCKED by commit_guard hook:\n- " + "\n- ".join(problems),
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)  # fail open — never brick the workflow
```

**Test coverage:** an 18-case test harness was run against this (good/bad formats,
attribution, banned files via `git add` in the same command, exempt repos, merge
commits, non-commit commands, bash heredoc, PowerShell here-string, malformed
stdin). All 18 passed before install. The test script itself was a throwaway in the
session scratchpad, not committed anywhere — if Codex needs to re-verify the hook
after modifying it, rebuild an equivalent harness rather than looking for that file.

**This mechanism is Claude-Code-specific** (the JSON-stdin/exit-code protocol, the
`settings.json` wiring). See §9 for how to port the *logic* to something
tool-agnostic.

---

## 7. Skills (global, in this repo)

Skills are markdown files with YAML frontmatter (`name`, `description`) that Claude
Code auto-discovers and can invoke when the description matches what's happening.
All three below are installed to `~/.claude/skills/<name>/SKILL.md`.

### `skills/new-repo-setup/SKILL.md`
```markdown
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
```

### `skills/verify-frontend-change/SKILL.md`
```markdown
---
name: verify-frontend-change
description: Verify any UI or frontend change end-to-end in a real browser before declaring it done. Trigger after editing anything user-visible - pages, components, styles, client demos - before reporting the work complete.
---

# Verifying Frontend Changes

Never report a UI change as complete based on a successful edit alone. Client
demos get seen by clients — "the edit applied" is not "it works".

## Steps

1. Start the dev server (use `.claude/launch.json` / preview tools if
   available) and open the edited page.
2. Interact with the change directly. For a new control (button, input,
   toggle): click it, confirm the expected state change actually happens.
3. Screenshot at desktop width AND mobile width (375px). Client demos are
   opened on phones.
4. Check the browser console: zero new errors or warnings.
5. Check network: no failed requests introduced by the change.
6. If any step fails, fix and rerun from step 1. Do not hand back partially
   verified work — report what was verified and how.

## For client demo work (Agency)

Additionally eyeball: hero section renders, primary CTA is visible and
clickable above the fold on mobile, no placeholder text or lorem ipsum left in.
```

### `skills/session-retro/SKILL.md`
```markdown
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
```

## Agency-local skills (NOT in dotfiles — live at `C:\CS\Agency\.claude\skills\`)

### `doc-sync/SKILL.md`
```markdown
---
name: doc-sync
description: Sync Agency docs per the Doc Update Matrix. Trigger at session end in the Agency workspace, and immediately after any strategy/ICP/offer/pricing decision, pipeline structure change, or pitch-logic edit.
---

# Agency Doc Sync

A change that leaves its doc stale is incomplete, not a follow-up. Walk this
checklist and update anything the session touched — in the same session.

## Checklist

1. **business_context.md** — did the session make/change an ICP, offer,
   channel, pricing, or market decision? Finish or kill an experiment? Lock an
   open decision? → Refresh the relevant section, the "Last updated" date, and
   the **LIVE OPEN DECISIONS** section so a fresh chat can resume cleanly.

2. **MEMORY.md** — any decision that would cost >1hr to reverse or touches a
   public interface? → Decisions table row with **why** + **what was
   rejected**. Every self-contained unit of work → one Session Log line.
   Refresh Next Session Priorities.

3. **ERRORS.md** — anything that took 2+ attempts or shipped a bug worth not
   repeating? → What broke / what worked / note for next time.

4. **PITCH_LOGIC.md** — did the session touch pitch-generation logic, the
   `hook_point` map, name-cleaning, or call-sheet formatting in
   `leads/src/generate_pitches_interior.py`? → Spec moves in the same edit as
   the code.

5. **leads/README.md** — did the session add/move/rename a script or data
   file, or change the pipeline run order? → Update the inventory + run order.

6. **CLAUDE.md** — did a new convention or hard rule get agreed? → Add it.

Report at the end which docs were updated and which were checked-but-current.
```

### `apify-run/SKILL.md`
```markdown
---
name: apify-run
description: Spend discipline for any paid scraping or lead-tool run (Apify actors, MillionVerifier, etc.). Trigger BEFORE starting any paid run and AFTER it completes.
---

# Paid Run Discipline

Lead scraping is the input to a test, not the deliverable. Never spend quietly.

## Before the run

1. Estimate cost from the actor's per-result pricing. If the estimate is over
   ~$2, state it explicitly and get a go-ahead before kicking off — especially
   when testing new limits/metros.
2. Right-size the raw pull: enough to cover the leads actually needed plus a
   filtering buffer. "Best list possible" means best ICP fit, not maximum
   dollars spent. Never spend the whole available balance on one batch.

## After the run

3. Pull REAL usage from the tool's own API/usage records (e.g. Apify run
   `usage_total_usd`) — never estimate-and-stay-quiet.
4. Report unprompted, immediately: total cost, what it bought (raw count vs.
   final filtered/delivered count), and what's left over as reusable inventory.
5. If the run exhausted one token/budget partway and fell back to a second,
   surface that explicitly — don't bury it.
6. Tag every lead with niche + metro + source before it enters the pipeline.
   Keep the no-email half (with phone numbers) for the phone/SMS channel.
```

---

## 8. Weekly review — `review/weekly_review.py` (v2) + `review/review_config.json`

**Trigger:** Windows Task Scheduler task `WeeklyClaudeReview`, runs Sundays 23:00,
registered via `~/.claude/register_weekly_review.bat`
(`schtasks /create /tn "WeeklyClaudeReview" /tr "...run_weekly_review.bat" /sc weekly /d SUN /st 23:00 /rl HIGHEST /f`).
`run_weekly_review.bat` sets PATH to Python 3.13 + npm, then runs
`python weekly_review.py >> weekly_review.log 2>&1`. This scheduling mechanism is
Windows-only and was not changed in the v2 rewrite.

**Scope (config-driven, `review_config.json`):**
```json
{
  "workspaces": ["C:\\CS\\Agency"],
  "extra_repos": [],
  "skip_remotes": [],
  "skip_dirs": ["node_modules", ".git", ".venv", "venv", "__pycache__", "Call Recordings"],
  "lookback_days": 7,
  "profile_repo": "C:\\Users\\athar\\wannabeaquant"
}
```
As of this handoff, scope is deliberately narrowed to **only the Agency workspace**
(per Atharva's explicit request — v1 scanned all of `C:\CS` including
non-actively-worked repos like alphafold3/numpy forks). Confirmed via dry-run to
discover 4 targets: the Agency workspace itself (non-git, read as context via
`business_context.md`), `Aperture`, `dezinepro-restyle`, `pribhum-nest`.
`kadiwa-studio` and `interior-shapes-designs` also exist under `C:\CS\Agency\demos`
but weren't in the dry-run output — worth Codex re-checking `find_targets()` picked
them up (nested one level under `demos/`, which the discovery logic should reach,
but this wasn't explicitly re-verified after the dry run).

**What changed from v1 → v2** (v1 no longer exists as a separate file, but its
behavior is documented here for context since PROFILE.md's auto-updated notes
reference patterns v1 detected):
- v1 scanned all of `C:\CS` with an allowlist/denylist of specific remotes; v2 scans
  configured workspace roots + their nested git repos, config-driven.
- v1 included non-git workspace roots not at all; v2 includes them as
  "CONTEXT-ONLY" targets (reads `business_context.md` if present) — this is how the
  Agency workspace itself (not a git repo) gets analyzed even though it has no
  commits of its own.
- v1 auto-committed and pushed CLAUDE.md updates and SESSION_NOTES.md to **project**
  repos. This directly contradicted the never-commit-context-files rule (§3, §9).
  v2 applies project-level CLAUDE.md updates and writes SESSION_NOTES.md **locally
  only** — never commits or pushes them to project repos. The one exception: the
  master `WEEKLY_REVIEW.md` in the separate `wannabeaquant/wannabeaquant` profile
  repo IS still committed/pushed — that repo is exempt (§9) and its whole purpose is
  to hold this report.
- v2 prompt adds two new sections: **"Claude Performance This Week"** (evidence-based
  got-right/got-wrong assessment from ERRORS.md + fix-commits chasing feat-commits +
  reverts) and **"Proposed Skills or Hooks"** (report-only, never auto-applied —
  the model is instructed to route deterministic-checkable issues here instead of
  into the prose CLAUDE.md-additions section).

**Full source** — read directly from `review/weekly_review.py` in this repo
(also installed at `~/.claude/weekly_review.py`); it's ~370 lines so not duplicated
here, but the logic is: discover targets from config → collect commits/context-file
contents per target → build one large prompt → pipe through
`claude --output-format text` (path hardcoded to
`C:\Users\athar\AppData\Roaming\npm\claude.cmd`, falls back to bare `claude` if that
path doesn't exist) → parse out `## Proposed X` sections by header string match →
auto-apply PROFILE.md and global CLAUDE.md additions verbatim, apply project-level
CLAUDE.md additions locally per-repo, write local-only SESSION_NOTES.md per active
repo → commit+push only the profile repo's `WEEKLY_REVIEW.md`.

**Manual run:** `python ~/.claude/weekly_review.py` (add `--dry-run` to preview
discovery + prompt without calling Claude or writing anything — this is what was
used to verify scope during setup).

**If Codex is expected to keep this running for the month:** the `run_claude()`
function shells out specifically to the `claude` CLI. If Claude Code won't be
installed/available during this period, this script will fail outright (not
gracefully) — decide explicitly whether to (a) leave it as-is since it only
*analyzes* git history regardless of which tool authored the commits and Claude
Code CLI can remain installed even if not the daily driver, or (b) point it at
Codex's own CLI instead. This was flagged to Atharva as an open question and not
yet resolved as of this handoff — ask him rather than assuming.

---

## 9. Known open items — do not silently "fix" these, they're pending Atharva's call

1. **Global CLAUDE.md "New Project Setup" section is stale/contradictory** (§3).
   The inline steps there still imply committing context files; the "Git & Commits"
   section right above it and the `new-repo-setup` skill both say never commit
   them, and the hook enforces never-commit. Not yet edited in the live file —
   flagged twice, not actioned.
2. **Server install not yet confirmed run.** `install.sh` was written and the
   one-liner given to Atharva, but there's no confirmation it's actually been run
   on the company SSH box yet.
3. **tmux speed/multitasking setup was being discussed, not yet built.** Atharva
   was hitting speed + multitasking friction using the VS Code Claude extension
   over Remote-SSH (every UI render round-trips over SSH; one extension pane per
   VS Code window is heavy). Agreed direction: run the CLI directly in `tmux` on
   the server (persists across disconnects, instant window switching) instead of
   through the extension's own pane, optionally combined with git worktrees for
   same-repo parallelism. Two options were on the table when this handoff was
   requested instead:
   - **Option A**: tmux config + a launcher script that opens a named session with
     a window per active project.
   - **Option B**: A, plus `git worktree` conventions for cases where two Claude/
     Codex instances need to work the same repo simultaneously.
   Neither was built — Atharva hadn't picked between A and A+B yet.
4. **Weekly review's Claude-CLI dependency during the Codex month** — see §8,
   last paragraph. Unresolved.
5. **Agency `demos/kadiwa-studio` and `interior-shapes-designs`** — exist on disk
   but weren't confirmed present in the weekly-review dry-run output; worth a
   re-check if the review starts silently missing them.

---

## 10. Memory system (Claude-Code-specific infra — read before assuming it ports)

Separate from all of the above: Claude Code has its own auto-memory mechanism,
project-scoped at `C:\Users\athar\.claude\projects\C--CS-Random\memory\`, indexed
by `MEMORY.md` in that same directory. Four types: `user` (who Atharva is),
`feedback` (corrections/confirmed approaches, with **Why** + **How to apply**),
`project` (ongoing work/decisions), `reference` (pointers to external systems).
Current index as of this handoff:

| File | Type | Description |
|------|------|-------------|
| career_profile.md | user | Complete career profile - AI job applications, comp, opportunities, communication style, decision framework |
| feedback_communication_style.md | feedback | Communication style and writing preferences - NO em dashes, no cringe corporate, startup-founder tone |
| project_polymarket_bot.md | project | Polymarket alpha bot — full architecture, strategies, file locations, known issues |
| user_profile.md | user | User profile and collaboration preferences |
| feedback_git_push.md | feedback | Always push to GitHub after changes to polymarket-bot |
| feedback_disk_cleanup_safety.md | feedback | Never delete cache-named folders during cleanup without inspecting contents — past incident lost Chrome passwords + Claude history |
| project_claude_dotfiles.md | project | claude-dotfiles repo — source of truth for Claude config (hooks, skills, weekly review v2), install scripts for Windows + SSH |
| feedback_context_files_never_committed.md | feedback | CLAUDE.md/MEMORY.md/ERRORS.md stay local + gitignored in project repos — never-commit rule supersedes older setup instruction |

This indexing + automatic-recall-into-context behavior is Claude Code harness
infrastructure — **not aware of any equivalent in Codex.** The files themselves are
plain markdown and readable by anything with filesystem access (same machine), but
nothing will automatically decide "this memory is relevant, load it" the way Claude
Code does. If continuity of these facts matters during the Codex month, they need
to be pointed to explicitly (e.g. referenced from a Codex instructions file) rather
than assumed to carry over.

---

## 11. Porting to Codex specifically — what maps, what doesn't, what's uncertain

This was worked through with Atharva already; repeating here so Codex has the same
context rather than re-deriving it.

**Maps cleanly (portable content, different filename):**
- `home/CLAUDE.md` + `PROFILE.md` content → Codex's global instructions. Codex uses
  the `AGENTS.md` convention (repo-root `AGENTS.md`, likely a global one too) — this
  is a real, growing cross-tool standard, not Claude-specific. Several of Atharva's
  repos already have an `AGENTS.md` sitting next to `CLAUDE.md` (e.g. Aperture) —
  worth checking those first since some port work may already be half-done.
- Project `MEMORY.md`/`ERRORS.md` → same content, just referenced from that
  project's `AGENTS.md` instead of `CLAUDE.md`.

**Needs a rework, but becomes strictly better regardless of tool:**
- `commit_guard.py`'s *logic* (§6) should become a real git hook (`commit-msg` or
  `pre-commit`, wired via `core.hooksPath`), not a Claude-Code PreToolUse hook. That
  enforces the same rules no matter which tool or human drives the commit. This is
  worth doing even independent of the Codex move.

**Does NOT port — do not assume or fabricate an equivalent:**
- The auto-memory system (§10) — Claude Code harness infrastructure. No known Codex
  equivalent. Facts can be dumped to a plain doc; the automatic recall behavior
  cannot.
- The `SKILL.md` skill-discovery mechanism (§7) — no confirmed Codex equivalent.
  Fold the actual steps from each skill into the relevant `AGENTS.md` as plain
  instructions instead of assuming Codex will discover a `SKILL.md` file the same
  way.

**Explicitly uncertain — verify against Codex's actual docs/`codex --help` rather
than trusting this document's assumptions:** exact Codex config file locations/
names, whether Codex has any hook-like extensibility point at all, and whether its
`AGENTS.md` support matches what's described above. This document was written from
general knowledge of Codex CLI, not verified against its current docs at the time
of writing.

---

## 12. Suggested first actions if you're Codex picking this up

1. Read this file fully (done, if you're reading this).
2. Check what Codex's actual global-instructions mechanism is (`codex --help`,
   its docs) and port §3/§4/§5 content into it — ask Atharva whether he wants the
   full personal profile (§3+§4) or the slim server profile (§5) as the baseline,
   given you'll likely be working across both his personal repos and possibly the
   company server.
3. Convert `commit_guard.py`'s logic into a real git hook per §11, if Atharva wants
   enforcement to survive the tool switch.
4. Do NOT silently resolve any of §9's open items — surface them and ask, exactly
   as this document does.
5. Leave `C:\CS\claude-dotfiles` and the Windows scheduled task alone unless
   Atharva explicitly asks you to touch them — they're Claude Code's own
   infrastructure and he'll be back on Claude Code in a month.
