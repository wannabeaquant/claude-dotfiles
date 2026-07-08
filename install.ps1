# Install claude-dotfiles into ~/.claude (Windows). Repo is the source of truth.
$ErrorActionPreference = "Stop"
$repo   = Split-Path -Parent $MyInvocation.MyCommand.Path
$claude = "$env:USERPROFILE\.claude"
$stamp  = Get-Date -Format "yyyyMMdd-HHmmss"
$backup = "$claude\backups\dotfiles-$stamp"

New-Item -ItemType Directory -Force $backup, "$claude\hooks", "$claude\skills" | Out-Null

foreach ($f in @("CLAUDE.md", "PROFILE.md", "settings.json", "weekly_review.py", "review_config.json")) {
    if (Test-Path "$claude\$f") { Copy-Item "$claude\$f" "$backup\$f" }
}

Copy-Item "$repo\home\CLAUDE.md"           "$claude\CLAUDE.md"       -Force
Copy-Item "$repo\home\PROFILE.md"          "$claude\PROFILE.md"      -Force
Copy-Item "$repo\settings.windows.json"    "$claude\settings.json"   -Force
Copy-Item "$repo\hooks\*"                  "$claude\hooks\"          -Force
Copy-Item "$repo\skills\*"                 "$claude\skills\"         -Recurse -Force
Copy-Item "$repo\review\weekly_review.py"  "$claude\weekly_review.py" -Force
Copy-Item "$repo\review\review_config.json" "$claude\review_config.json" -Force

Write-Host "[OK] Installed to $claude"
Write-Host "[OK] Backup of previous config: $backup"
