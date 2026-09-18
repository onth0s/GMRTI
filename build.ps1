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

if ($CheckOnly -and $SkipFormat) {
    Write-Warning "Both -CheckOnly and -SkipFormat were specified: -CheckOnly already skips formatting. Verification may fail if files are unformatted."
}

# Calculate dynamic step count based on active flags
$totalSteps = 0
if (-not $CheckOnly -and -not $SkipFormat) { $totalSteps++ }
if (-not $CheckOnly) { $totalSteps++ }
$totalSteps += 2  # sync check and format check always run
if (-not $SkipTests) { $totalSteps++ }

$step = 0

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " GMRTI Build Pipeline" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# 1. Format
if (-not $CheckOnly -and -not $SkipFormat) {
    $step++
    Write-Host "`n[$step/$totalSteps] Formatting files (wrap.py)..." -ForegroundColor Yellow
    python wrap.py
    if ($LASTEXITCODE -ne 0) {
        Write-Error "wrap.py formatting failed."
        exit 1
    }
}

# 2. Compile monolithic treatise
if (-not $CheckOnly) {
    $step++
    Write-Host "`n[$step/$totalSteps] Compiling monolithic treatise (rewrite.py)..." -ForegroundColor Yellow
    python rewrite.py
    if ($LASTEXITCODE -ne 0) {
        Write-Error "rewrite.py compilation failed."
        exit 1
    }
}

# 3. Verify monolithic sync
$step++
Write-Host "`n[$step/$totalSteps] Verifying monolithic document sync (rewrite.py --check)..." -ForegroundColor Yellow
python rewrite.py --check
if ($LASTEXITCODE -ne 0) {
    Write-Error "rewrite.py --check failed: monolithic document is out of sync."
    exit 1
}

# 4. Verify formatting
$step++
Write-Host "`n[$step/$totalSteps] Verifying formatting (wrap.py --check)..." -ForegroundColor Yellow
python wrap.py --check
if ($LASTEXITCODE -ne 0) {
    Write-Error "wrap.py --check failed: unformatted files detected."
    exit 1
}

# 5. Run test suite
if (-not $SkipTests) {
    $step++
    Write-Host "`n[$step/$totalSteps] Running test suite (pytest)..." -ForegroundColor Yellow
    python -m pytest tests/ -v
    if ($LASTEXITCODE -ne 0) {
        Write-Error "pytest test suite failed."
        exit 1
    }
}

Write-Host "`n==================================================" -ForegroundColor Green
Write-Host " Build succeeded! All artifacts up to date and verified." -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
exit 0
