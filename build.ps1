<#
.SYNOPSIS
    Full build pipeline for GMRTI.

.DESCRIPTION
    When run bare (without flags), builds everything:
    1. Formats all markdown and YAML files (wrap.py)
    2. Recompiles the monolithic document and archives prior revisions (rewrite.py)
    3. Verifies monolithic sync (rewrite.py --check)
    4. Verifies formatting (wrap.py --check)
    5. Runs the full pytest test suite

    Flags are optional bypasses.

.PARAMETER CheckOnly
    Skip formatting and compilation; only verify sync, format, and tests.

.PARAMETER SkipTests
    Skip running pytest.

.PARAMETER SkipFormat
    Skip the in-place formatting step.
#>
[CmdletBinding()]
param(
    [switch]$CheckOnly,
    [switch]$SkipTests,
    [switch]$SkipFormat
)

$ErrorActionPreference = "Stop"

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " GMRTI Build Pipeline" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# 1. Format
if (-not $CheckOnly -and -not $SkipFormat) {
    Write-Host "`n[1/5] Formatting files (wrap.py)..." -ForegroundColor Yellow
    python wrap.py
    if ($LASTEXITCODE -ne 0) {
        Write-Error "wrap.py formatting failed."
        exit 1
    }
}

# 2. Compile monolithic treatise
if (-not $CheckOnly) {
    Write-Host "`n[2/5] Compiling monolithic treatise (rewrite.py)..." -ForegroundColor Yellow
    python rewrite.py
    if ($LASTEXITCODE -ne 0) {
        Write-Error "rewrite.py compilation failed."
        exit 1
    }
}

# 3. Verify monolithic sync
Write-Host "`n[3/5] Verifying monolithic document sync (rewrite.py --check)..." -ForegroundColor Yellow
python rewrite.py --check
if ($LASTEXITCODE -ne 0) {
    Write-Error "rewrite.py --check failed: monolithic document is out of sync."
    exit 1
}

# 4. Verify formatting
Write-Host "`n[4/5] Verifying formatting (wrap.py --check)..." -ForegroundColor Yellow
python wrap.py --check
if ($LASTEXITCODE -ne 0) {
    Write-Error "wrap.py --check failed: unformatted files detected."
    exit 1
}

# 5. Run test suite
if (-not $SkipTests) {
    Write-Host "`n[5/5] Running test suite (pytest)..." -ForegroundColor Yellow
    python -m pytest tests/ -v
    if ($LASTEXITCODE -ne 0) {
        Write-Error "pytest test suite failed."
        exit 1
    }
}

Write-Host "`n==================================================" -ForegroundColor Green
Write-Host " Build succeeded! All artifacts up to date and verified." -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
