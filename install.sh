#!/usr/bin/env bash
# Install claude-dotfiles into ~/.claude (Linux/macOS server profile).
# Installs the slim server CLAUDE.md (no personal project context), hooks, skills.
set -euo pipefail

repo="$(cd "$(dirname "$0")" && pwd)"
claude="$HOME/.claude"
stamp="$(date +%Y%m%d-%H%M%S)"

mkdir -p "$claude/hooks" "$claude/skills" "$claude/backups"

[ -f "$claude/CLAUDE.md" ] && cp "$claude/CLAUDE.md" "$claude/backups/CLAUDE.md.$stamp"
cp "$repo/server/CLAUDE.md" "$claude/CLAUDE.md"
cp "$repo/hooks/"*.py "$claude/hooks/"
cp -r "$repo/skills/"* "$claude/skills/"

PY="$(command -v python3 || command -v python)"
hook_cmd="$PY $claude/hooks/commit_guard.py"

if [ ! -f "$claude/settings.json" ]; then
  cat > "$claude/settings.json" <<EOF
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "$hook_cmd" }
        ]
      }
    ]
  }
}
EOF
  echo "[OK] settings.json created with commit_guard hook"
else
  cp "$claude/settings.json" "$claude/backups/settings.json.$stamp"
  echo "[!] $claude/settings.json already exists (backed up). Add this hook to it manually:"
  echo '    "hooks": { "PreToolUse": [ { "matcher": "Bash", "hooks": [ { "type": "command", "command": "'"$hook_cmd"'" } ] } ] }'
fi

echo "[OK] Server profile installed to $claude"
echo "    Note: weekly review is not installed on servers (runs on the Windows box only)."
