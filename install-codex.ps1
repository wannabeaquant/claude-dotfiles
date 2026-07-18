# Install the Codex profile without modifying the existing Claude Code setup.
$ErrorActionPreference = "Stop"

$repo = Split-Path -Parent $MyInvocation.MyCommand.Path
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { "$env:USERPROFILE\.codex" }
$skillHome = "$env:USERPROFILE\.agents\skills"
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backup = "$codexHome\backups\dotfiles-$stamp"
$legacyMemory = "$codexHome\legacy-memory"
$claudeMemory = "$env:USERPROFILE\.claude\projects\C--CS-Random\memory"

New-Item -ItemType Directory -Force $backup, $skillHome, "$codexHome\git-hooks", $legacyMemory | Out-Null

foreach ($file in @("AGENTS.md", "config.toml")) {
    if (Test-Path "$codexHome\$file") {
        Copy-Item "$codexHome\$file" "$backup\$file" -Force
    }
}

$previousHooksPath = git config --global --get core.hooksPath
if ($LASTEXITCODE -eq 0 -and $previousHooksPath) {
    Set-Content -LiteralPath "$backup\previous-core-hooksPath.txt" -Value $previousHooksPath
}

Copy-Item "$repo\codex\home\AGENTS.md" "$codexHome\AGENTS.md" -Force
Copy-Item "$repo\codex\git-hooks\*" "$codexHome\git-hooks\" -Force

foreach ($skill in Get-ChildItem "$repo\codex\skills" -Directory) {
    $destination = Join-Path $skillHome $skill.Name
    if (Test-Path $destination) {
        Copy-Item $destination "$backup\skill-$($skill.Name)" -Recurse -Force
    }
    New-Item -ItemType Directory -Force $destination | Out-Null
    Copy-Item "$($skill.FullName)\*" $destination -Recurse -Force
}

if (Test-Path $claudeMemory) {
    if (Get-ChildItem $legacyMemory -Force -ErrorAction SilentlyContinue) {
        Copy-Item $legacyMemory "$backup\legacy-memory" -Recurse -Force
    }
    Copy-Item "$claudeMemory\*.md" $legacyMemory -Force
}

git config --global core.hooksPath "$codexHome\git-hooks"
if ($LASTEXITCODE -ne 0) { throw "Failed to configure global Git hooks" }

$codex = Get-Command codex -ErrorAction SilentlyContinue
if ($codex) {
    & $codex.Source features enable memories
    if ($LASTEXITCODE -ne 0) { throw "Failed to enable Codex memories" }
} else {
    Write-Warning "Codex CLI not found. Enable the memories feature manually in config.toml."
}

Write-Host "[OK] Installed Codex guidance to $codexHome\AGENTS.md"
Write-Host "[OK] Installed global skills to $skillHome"
Write-Host "[OK] Migrated historical memory files to $legacyMemory"
Write-Host "[OK] Installed tool-independent Git hooks to $codexHome\git-hooks"
Write-Host "[OK] Backup of previous Codex config: $backup"
Write-Host "[NOTE] Restart Codex so new global guidance and skills are discovered."
