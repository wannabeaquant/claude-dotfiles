"""Weekly pattern review v2 — analyzes the repos Atharva is actively working on.

Config-driven (~/.claude/review_config.json): scans configured workspace roots
(git or not) plus nested git repos, feeds the week's commits + context files
through the Claude CLI, writes WEEKLY_REVIEW.md to the profile repo, and
auto-applies proposed PROFILE.md / global CLAUDE.md additions.

v2 changes vs v1:
  - Repo discovery is scoped to config workspaces, not all of C:\\CS
  - Non-git workspace roots (e.g. C:\\CS\\Agency) are included as context
  - New prompt sections: Claude performance (right/wrong) + proposed skills/hooks
  - Project CLAUDE.md updates and SESSION_NOTES.md are applied LOCALLY ONLY,
    never committed (context files are gitignored per global rules)
"""
import subprocess
import sys
import os
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

# Force UTF-8 output on Windows
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

CLAUDE_DIR = Path.home() / ".claude"
CONFIG_PATH = CLAUDE_DIR / "review_config.json"

DEFAULT_CONFIG = {
    "workspaces": [r"C:\CS\Agency"],
    "extra_repos": [],
    "skip_remotes": [],
    "skip_dirs": ["node_modules", ".git", ".venv", "venv", "__pycache__"],
    "lookback_days": 7,
    "profile_repo": str(Path.home() / "wannabeaquant"),
}

DRY_RUN = "--dry-run" in sys.argv


def load_config():
    cfg = dict(DEFAULT_CONFIG)
    if CONFIG_PATH.exists():
        try:
            cfg.update(json.loads(CONFIG_PATH.read_text(encoding="utf-8")))
        except Exception as e:
            print(f"WARN could not parse {CONFIG_PATH}: {e} — using defaults")
    return cfg


# ── Helpers ───────────────────────────────────────────────────────────────────

def run(cmd, cwd=None, capture=True):
    r = subprocess.run(cmd, cwd=cwd, capture_output=capture, text=True, shell=True)
    return r.stdout.strip() if capture else r.returncode


def git_remote(path):
    raw = run(f'git -C "{path}" remote get-url origin 2>nul', cwd=path)
    if not raw:
        raw = run(f'git -C "{path}" remote get-url downstream 2>nul', cwd=path)
    if not raw:
        return None
    raw = raw.replace("https://github.com/", "").replace("git@github.com:", "")
    raw = raw.rstrip("/").removesuffix(".git")
    return raw or None


def commits_since(path, days):
    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    return run(f'git -C "{path}" log --oneline --since={since}')


def commit_types_since(path, days):
    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    msgs = run(f'git -C "{path}" log --format=%s --since={since}')
    if not msgs:
        return {}
    counts = {}
    for m in msgs.splitlines():
        t = m.split("(")[0].split(":")[0].strip().lower()
        counts[t] = counts.get(t, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: -x[1]))


def read_file(path, max_lines=80):
    p = Path(path)
    if not p.exists():
        return None
    lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
    if len(lines) > max_lines:
        lines = lines[:max_lines] + [f"... ({len(lines) - max_lines} more lines)"]
    return "\n".join(lines)


def format_commit_score(msgs):
    """1-5 score for commit message format compliance."""
    if not msgs:
        return "N/A (no commits)"
    lines = [l for l in msgs.splitlines() if l.strip()]
    ok = sum(1 for l in lines if ":" in l and "(" in l)
    score = round(1 + 4 * ok / max(len(lines), 1))
    return f"{score}/5"


# ── Discover targets ──────────────────────────────────────────────────────────

def find_targets(cfg):
    """Workspace roots (git or not) + nested git repos (depth 2) + extra repos."""
    targets = []
    seen = set()

    def add(path, kind):
        p = Path(path)
        key = str(p).lower()
        if key in seen or not p.exists():
            return
        seen.add(key)
        is_git = (p / ".git").exists()
        targets.append({
            "path": p,
            "kind": kind,
            "is_git": is_git,
            "remote": git_remote(p) if is_git else None,
        })

    skip_dirs = {d.lower() for d in cfg["skip_dirs"]}
    for ws in cfg["workspaces"]:
        ws = Path(ws)
        if not ws.exists():
            print(f"WARN workspace not found: {ws}")
            continue
        add(ws, "workspace")
        for d in ws.iterdir():
            if not d.is_dir() or d.name.lower() in skip_dirs:
                continue
            if (d / ".git").exists():
                add(d, "repo")
            else:
                for dd in d.iterdir():
                    if dd.is_dir() and dd.name.lower() not in skip_dirs and (dd / ".git").exists():
                        add(dd, "repo")

    for p in cfg["extra_repos"]:
        add(p, "repo")

    skip_remotes = {s.lower() for s in cfg["skip_remotes"]}
    return [t for t in targets if (t["remote"] or "").lower() not in skip_remotes or t["remote"] is None]


# ── Collect data ──────────────────────────────────────────────────────────────

def collect(targets, cfg):
    days = cfg["lookback_days"]
    data = []
    for t in targets:
        path = t["path"]
        name = t["remote"] or path.name
        commits = commits_since(path, days) if t["is_git"] else ""
        d = {
            "repo": name,
            "path": str(path),
            "kind": t["kind"],
            "is_git": t["is_git"],
            "commits": commits,
            "types": commit_types_since(path, days) if t["is_git"] else {},
            "score": format_commit_score(commits) if t["is_git"] else "N/A (not a git repo)",
            "active": bool(commits.strip()),
            "claude": read_file(path / "CLAUDE.md"),
            "memory": read_file(path / "MEMORY.md", max_lines=100),
            "errors": read_file(path / "ERRORS.md", max_lines=100),
            "readme": read_file(path / "README.md", max_lines=30),
            "context": read_file(path / "business_context.md", max_lines=60) if t["kind"] == "workspace" else None,
            "new": t["is_git"] and not (path / "CLAUDE.md").exists(),
        }
        data.append(d)
    return data


# ── Build prompt ──────────────────────────────────────────────────────────────

def build_prompt(data, today, days):
    sections = []
    sections.append(
        f"Today is {today}. You are analyzing the past {days} days of work for "
        "Atharva Singh (wannabeaquant) across his ACTIVE projects only."
    )
    sections.append(
        "Your job: extract patterns, assess commit health, assess how well Claude "
        "(his coding agent) performed, and propose specific improvements to his "
        "rules, skills, and hooks. Be evidence-based — only propose what this "
        "week's data clearly supports.\n"
    )

    for d in data:
        label = "WORKSPACE" if d["kind"] == "workspace" else "REPO"
        status = "ACTIVE" if d["active"] else ("QUIET" if d["is_git"] else "CONTEXT-ONLY")
        sections.append(f"═══ {label}: {d['repo']} ({status}) ═══")
        sections.append(f"Path: {d['path']}")

        if d["commits"]:
            sections.append(f"\n--- Commits this week ---\n{d['commits']}")
            sections.append(f"Type breakdown: {json.dumps(d['types'])}")
            sections.append(f"Format score: {d['score']}")
        elif d["is_git"]:
            sections.append("No commits this week.")

        if d["new"]:
            sections.append("WARN  NEW REPO — no CLAUDE.md yet")

        if d["context"]:
            sections.append(f"\n--- business_context.md ---\n{d['context']}")
        if d["memory"]:
            sections.append(f"\n--- MEMORY.md ---\n{d['memory']}")
        if d["errors"]:
            sections.append(f"\n--- ERRORS.md ---\n{d['errors']}")
        if d["claude"]:
            sections.append(f"\n--- CLAUDE.md (current) ---\n{d['claude']}")
        elif d["readme"]:
            sections.append(f"\n--- README.md (no CLAUDE.md yet) ---\n{d['readme']}")
        sections.append("")

    sections.append("""
─────────────────────────────────────────────
OUTPUT: Write a WEEKLY_REVIEW.md with this exact structure:

# Weekly Pattern Review — DATE

## Repos Analyzed This Week
| Repo | Commits | Format Score | Status |
|------|---------|--------------|--------|
(one row per repo/workspace in the data above)

## New Projects Detected
(repos flagged as NEW above — list them and note they need CLAUDE.md setup)
(write "None" if no new repos)

## Work Summary
(per-repo bullet: what was actually committed / decided, 1-2 lines. Skip quiet repos.)

## Commit Health
(flag repos with 0 commits, flag repos with format score < 3/5, note any patterns)

## Claude Performance This Week
Evidence-based assessment of how the coding agent did, from ERRORS.md entries,
fix-commits chasing feat-commits, revert commits, and repeated attempts:
- **Got right:** approaches that worked and are worth repeating
- **Got wrong:** mistakes with evidence, and whether they are first-time or repeats

## Patterns Observed This Week
(evidence-based cross-repo patterns — what Atharva consistently does/avoids)

## Recurring Issues
(from ERRORS.md + commit patterns — flag anything appearing in 2+ repos or sessions)
(write "None" if nothing recurring)

## Proposed Skills or Hooks
(REPORT ONLY, never auto-applied. If a recurring mistake would be better fixed by
a deterministic hook or a reusable skill than a prose rule, describe it concretely:
name, trigger, what it checks/does. Hooks live in claude-dotfiles/hooks/, skills in
claude-dotfiles/skills/. Write "None" if nothing warranted.)

## Proposed Global CLAUDE.md Additions
CRITICAL FORMAT: write "None" if nothing warranted. Otherwise write ONLY the exact
rule lines to append (no preamble, evidence as inline comment). These will be
auto-appended to ~/.claude/CLAUDE.md verbatim. Only judgment-call rules belong
here — anything deterministic belongs in Proposed Skills or Hooks instead.

## Proposed Project-Level CLAUDE.md Updates
CRITICAL FORMAT: write "None" if nothing warranted. Otherwise use EXACTLY this
structure — one ### block per repo, repo name matching the data above:

### repo-name-here
(exact lines to append to that repo's CLAUDE.md — no preamble)

These are applied to each repo's LOCAL CLAUDE.md (never committed). Skip any repo
with nothing new.

## MEMORY.md Entries Suggested
(per-repo — decisions made this week worth logging permanently)

## Proposed PROFILE.md Additions
CRITICAL FORMAT: write "None" if nothing warranted. Otherwise write ONLY the exact
lines to append (no preamble). Auto-appended to ~/.claude/PROFILE.md under
"## Auto-Updated". Only observations about HOW Atharva works — preferences,
patterns, tendencies — not project-specific facts.

## Next Week Watch List
- (2-3 specific things to pay attention to next week)
─────────────────────────────────────────────
Write ONLY the markdown. No preamble. No explanation. Just the file content.
""")
    return "\n".join(sections)


# ── Run Claude CLI ─────────────────────────────────────────────────────────────

def run_claude(prompt):
    import tempfile
    claude_cmd = str(Path.home() / "AppData" / "Roaming" / "npm" / "claude.cmd")
    if not Path(claude_cmd).exists():
        claude_cmd = "claude"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False,
                                     encoding="utf-8", errors="ignore") as f:
        f.write(prompt)
        tmpfile = f.name
    try:
        result = subprocess.run(
            f'type "{tmpfile}" | "{claude_cmd}" --output-format text',
            shell=True, capture_output=True, text=True,
            encoding="utf-8", errors="ignore",
        )
        if result.returncode != 0:
            print(f"[claude CLI error]\n{result.stderr}", file=sys.stderr)
            return None
        return result.stdout.strip() or None
    finally:
        try:
            os.unlink(tmpfile)
        except OSError:
            pass


# ── Per-repo SESSION_NOTES.md (local only — never committed) ─────────────────

SESSION_NOTES_PROMPT = """
Given this repo's commits this week and its current CLAUDE.md/MEMORY.md/ERRORS.md,
write a SHORT SESSION_NOTES.md (max 30 lines) with this structure:

# Session Notes — DATE

## This Week
(3-5 bullets: what shipped)

## Proposed CLAUDE.md Update
(exact text to add — skip section entirely if nothing new)

## MEMORY.md Entry
(if any decision was made worth logging — skip if none)

## Watch Next Week
(1 specific thing)

Write ONLY the markdown. No preamble.

REPO DATA:
"""


def write_session_notes(d, today):
    if not d["active"]:
        return
    prompt = SESSION_NOTES_PROMPT.replace("DATE", today) + f"""
Repo: {d['repo']}
Commits: {d['commits']}
CLAUDE.md: {d['claude'] or 'none'}
MEMORY.md: {d['memory'] or 'none'}
ERRORS.md: {d['errors'] or 'none'}
"""
    notes = run_claude(prompt)
    if not notes:
        return
    (Path(d["path"]) / "SESSION_NOTES.md").write_text(notes, encoding="utf-8")
    print(f"  SESSION_NOTES → {d['repo']} (local only, not committed)")


# ── Auto-apply proposals ─────────────────────────────────────────────────────

def extract_section(text, header):
    lines = text.splitlines()
    collecting = False
    out = []
    for line in lines:
        if line.startswith("## ") and header.lower() in line.lower():
            collecting = True
            continue
        if collecting:
            if line.startswith("## "):
                break
            out.append(line)
    return "\n".join(out).strip()


SKIP_PHRASES = {"none", "(skip)", "skip", "nothing", "n/a", ""}


def meaningful_lines(content):
    return [l for l in content.splitlines() if l.strip() and not l.strip().startswith("(")]


def apply_profile_additions(content, today):
    if content.lower().strip() in SKIP_PHRASES:
        return False
    meaningful = meaningful_lines(content)
    if not meaningful:
        return False
    profile = CLAUDE_DIR / "PROFILE.md"
    if not profile.exists():
        return False
    existing = profile.read_text(encoding="utf-8", errors="ignore").rstrip()
    addition = f"\n\n### {today}\n" + "\n".join(f"- {l.lstrip('- ')}" for l in meaningful)
    if "## Auto-Updated" not in existing:
        addition = "\n\n## Auto-Updated" + addition
    profile.write_text(existing + addition + "\n", encoding="utf-8")
    print(f"[apply] PROFILE.md updated with {len(meaningful)} observation(s)")
    return True


def apply_global_additions(content, today):
    if content.lower().strip() in SKIP_PHRASES:
        return False
    meaningful = meaningful_lines(content)
    if not meaningful:
        return False
    global_claude = CLAUDE_DIR / "CLAUDE.md"
    existing = global_claude.read_text(encoding="utf-8", errors="ignore")
    global_claude.write_text(existing + f"\n\n## Auto-Added {today}\n{content}\n", encoding="utf-8")
    print(f"[apply] Global CLAUDE.md updated with {len(meaningful)} new rule(s)")
    return True


def apply_project_additions(content, data, today):
    """Append per-repo blocks to each project's LOCAL CLAUDE.md. Never commits."""
    import re
    if content.lower().strip() in SKIP_PHRASES:
        return []
    path_map = {d["repo"].lower(): Path(d["path"]) for d in data}
    applied = []
    for block in re.split(r"(?:^|\n)### ", content):
        if not block.strip():
            continue
        lines = block.strip().splitlines()
        repo_name = lines[0].strip()
        addition = "\n".join(lines[1:]).strip()
        if not meaningful_lines(addition):
            continue
        repo_path = path_map.get(repo_name.lower())
        if not repo_path:
            print(f"  WARN no local path for {repo_name} — skipping")
            continue
        claude_md = repo_path / "CLAUDE.md"
        if not claude_md.exists():
            continue
        existing = claude_md.read_text(encoding="utf-8", errors="ignore")
        claude_md.write_text(existing + f"\n\n## Auto-Added {today}\n{addition}\n", encoding="utf-8")
        print(f"  [apply] {repo_name} CLAUDE.md updated (local only, not committed)")
        applied.append(repo_name)
    return applied


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    cfg = load_config()
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"\n{'=' * 60}")
    print(f"  Weekly Pattern Review v2 — {today}")
    print(f"{'=' * 60}\n")

    print(f"[*] Scanning workspaces: {', '.join(cfg['workspaces'])}")
    targets = find_targets(cfg)
    data = collect(targets, cfg)

    active_count = sum(1 for d in data if d["active"])
    print(f"   {len(data)} targets ({active_count} with commits this week)\n")
    for d in data:
        flag = "ACTIVE" if d["active"] else ("quiet" if d["is_git"] else "context")
        new = " [NEW]" if d["new"] else ""
        n_commits = len(d["commits"].splitlines()) if d["commits"] else 0
        print(f"   {flag:7} {d['repo']}{new} — {n_commits} commits")

    if DRY_RUN:
        print("\n[DRY RUN] Skipping Claude analysis and apply.")
        print("\nPrompt preview:\n")
        print(build_prompt(data, today, cfg["lookback_days"])[:2000], "...")
        return

    print("\n[AI] Running Claude analysis...")
    review = run_claude(build_prompt(data, today, cfg["lookback_days"]))
    if not review:
        print("ERROR Claude returned no output. Aborting.")
        sys.exit(1)

    # Write master review to profile repo (the one intentional push)
    profile_path = Path(cfg["profile_repo"])
    if not profile_path.exists():
        print("   Cloning wannabeaquant/wannabeaquant...")
        run(f'git clone https://github.com/wannabeaquant/wannabeaquant "{profile_path}"', capture=False)

    (profile_path / "WEEKLY_REVIEW.md").write_text(review, encoding="utf-8")
    print(f"\n[write] WEEKLY_REVIEW.md → {profile_path}")
    run(f'git -C "{profile_path}" add WEEKLY_REVIEW.md', capture=False)
    run(f'git -C "{profile_path}" commit -m "docs(review): weekly pattern analysis {today}"', capture=False)
    push_out = run(f'git -C "{profile_path}" push 2>&1')
    print("OK pushed to profile repo" if ("main" in push_out or push_out == "") else f"WARN push: {push_out[:100]}")

    print("\n[apply] Applying proposed updates...")
    apply_profile_additions(extract_section(review, "Proposed PROFILE.md Additions"), today)
    apply_global_additions(extract_section(review, "Proposed Global CLAUDE.md Additions"), today)
    applied = apply_project_additions(extract_section(review, "Proposed Project-Level CLAUDE.md Updates"), data, today)
    if not applied:
        print("  (no project-level changes this week)")

    proposals = extract_section(review, "Proposed Skills or Hooks")
    if proposals and proposals.lower().strip() not in SKIP_PHRASES:
        print(f"\n[proposals] Skills/hooks suggested this week (review in WEEKLY_REVIEW.md):\n{proposals}")

    print("\n[notes] Writing per-repo SESSION_NOTES.md (local only)...")
    for d in data:
        write_session_notes(d, today)

    print(f"\nOK Done. https://github.com/wannabeaquant/wannabeaquant/blob/main/WEEKLY_REVIEW.md")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
