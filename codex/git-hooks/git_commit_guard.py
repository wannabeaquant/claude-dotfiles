#!/usr/bin/env python3
"""Shared policy for the global pre-commit and commit-msg hooks."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


TYPES = "feat|fix|refactor|test|docs|chore|perf"
SUBJECT_RE = re.compile(rf"^({TYPES})\([^)]+\): \S")
EXEMPT_SUBJECT_RE = re.compile(r"^(merge|revert|fixup!|squash!|initial commit)", re.I)
ATTRIBUTION_RE = re.compile(
    r"co-authored-by\s*:[^\n]*(claude|anthropic|openai|codex)"
    r"|generated with[^\n]*(claude|anthropic|openai|codex)",
    re.I,
)
BANNED_FILES = {
    "agents.md",
    "claude.md",
    "errors.md",
    "memory.md",
    "profile.md",
    "session_notes.md",
}
BANNED_DIRS = {".agents", ".claude"}
EXEMPT_REPOS = {"claude-dotfiles", "dotfiles", "wannabeaquant"}


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], capture_output=True, text=True, encoding="utf-8", errors="replace"
    )


def repo_name() -> str:
    result = git("rev-parse", "--show-toplevel")
    if result.returncode != 0 or not result.stdout.strip():
        return ""
    return Path(result.stdout.strip()).name.lower()


def staged_files() -> list[str]:
    result = git("diff", "--cached", "--name-only", "--diff-filter=ACMR")
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def banned_paths(paths: list[str]) -> list[str]:
    hits: list[str] = []
    for path in paths:
        parts = path.replace("\\", "/").lower().split("/")
        if parts[-1] in BANNED_FILES or any(part in BANNED_DIRS for part in parts):
            hits.append(path)
    return hits


def validate_pre_commit() -> list[str]:
    if repo_name() in EXEMPT_REPOS:
        return []
    hits = banned_paths(staged_files())
    if not hits:
        return []
    return [
        "personal context files must stay local in project repos: " + ", ".join(hits)
    ]


def validate_commit_message(path: Path) -> list[str]:
    message = path.read_text(encoding="utf-8", errors="replace")
    problems: list[str] = []
    if ATTRIBUTION_RE.search(message):
        problems.append("remove AI attribution; commits are authored by Atharva only")

    subject = message.strip().splitlines()[0].strip() if message.strip() else ""
    if not subject:
        problems.append("commit message is empty")
    elif not EXEMPT_SUBJECT_RE.match(subject) and not SUBJECT_RE.match(subject):
        problems.append(
            f'commit subject "{subject}" must match <type>(<scope>): <description>; '
            f"allowed types: {TYPES.replace('|', ', ')}"
        )
    return problems


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] not in {"pre-commit", "commit-msg"}:
        print("usage: git_commit_guard.py pre-commit | commit-msg <message-file>", file=sys.stderr)
        return 2

    if argv[1] == "pre-commit":
        problems = validate_pre_commit()
    elif len(argv) == 3:
        problems = validate_commit_message(Path(argv[2]))
    else:
        print("commit-msg requires the commit message file", file=sys.stderr)
        return 2

    if problems:
        print("COMMIT BLOCKED by git_commit_guard:\n- " + "\n- ".join(problems), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
