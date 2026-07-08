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
