<#
.SYNOPSIS
    Purges content from addressed update-cycle Markdown logs while keeping the files.

.DESCRIPTION
    Resets DISSONANCE.md, refinery/DISSONANCE.md, DECISIONS.md, and PLAN.md to
    minimal placeholder headers after an audit/refinement cycle has been resolved
    and ratified. Prompts for confirmation unless -Force is passed.
#>
[CmdletBinding()]
param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$targets = [ordered]@{
    "DISSONANCE.md"          = "# GMRTI Adversarial Audit Log: Dissonance Report`n`n*No active dissonances.*`n"
    "refinery/DISSONANCE.md" = "# Refinery Adversarial Audit Log`n`n*No active dissonances.*`n"
    "DECISIONS.md"           = "# GMRTI Decision Log`n`n*No active decisions.*`n"
    "PLAN.md"                = "# GMRTI Ratified Execution Plan`n`n*No active execution plan.*`n"
}

Write-Host "==================================================" -ForegroundColor Yellow
Write-Host " GMRTI Update-Cycle Purge (nuke.ps1)" -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Yellow
Write-Host "The following files will be purged (content cleared, files kept):"
foreach ($rel in $targets.Keys) {
    Write-Host "  - $rel" -ForegroundColor Cyan
}

if (-not $Force) {
    $reply = Read-Host "`nProceed with purge? [y/N]"
    if ($reply -notin @("y", "Y", "yes", "YES")) {
        Write-Host "Aborted. No files were modified." -ForegroundColor Gray
        exit 0
    }
}

$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
foreach ($rel in $targets.Keys) {
    $fullPath = Join-Path $PSScriptRoot $rel
    if (-not (Test-Path $fullPath)) {
        Write-Host "Skipped (not found): $rel" -ForegroundColor DarkYellow
        continue
    }
    [System.IO.File]::WriteAllText($fullPath, $targets[$rel], $utf8NoBom)
    Write-Host "Purged: $rel" -ForegroundColor Green
}

Write-Host "`nDone. Run '.\build.ps1 -CheckOnly' to verify repository state." -ForegroundColor Cyan
exit 0
