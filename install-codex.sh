#!/usr/bin/env bash
# Install the slim Codex server profile. Does not modify ~/.claude.
set -euo pipefail

repo="$(cd "$(dirname "$0")" && pwd)"
codex_home="${CODEX_HOME:-$HOME/.codex}"
skill_home="$HOME/.agents/skills"
stamp="$(date +%Y%m%d-%H%M%S)"
backup="$codex_home/backups/dotfiles-$stamp"

mkdir -p "$backup" "$skill_home" "$codex_home/git-hooks"
[ -f "$codex_home/AGENTS.md" ] && cp "$codex_home/AGENTS.md" "$backup/AGENTS.md"
[ -f "$codex_home/config.toml" ] && cp "$codex_home/config.toml" "$backup/config.toml"

previous_hooks_path="$(git config --global --get core.hooksPath || true)"
[ -n "$previous_hooks_path" ] && printf '%s\n' "$previous_hooks_path" > "$backup/previous-core-hooksPath.txt"

cp "$repo/codex/server/AGENTS.md" "$codex_home/AGENTS.md"
cp "$repo/codex/git-hooks/"* "$codex_home/git-hooks/"
chmod +x "$codex_home/git-hooks/pre-commit" "$codex_home/git-hooks/commit-msg"
cp -r "$repo/codex/skills/"* "$skill_home/"
git config --global core.hooksPath "$codex_home/git-hooks"

if command -v codex >/dev/null 2>&1; then
  codex features enable memories
else
  echo "[!] Codex CLI not found. Enable the memories feature manually in config.toml."
fi

echo "[OK] Slim Codex server profile installed to $codex_home"
echo "[OK] Global skills installed to $skill_home"
echo "[OK] Backup created at $backup"
