<#
.SYNOPSIS
    Full build pipeline for GMRTI.

.DESCRIPTION
    When run bare (without flags), builds everything:
    1. Formats all markdown and YAML files (wrap.py)
    2. Recompiles the monolithic document and archives prior revisions (rewrite.py)
    3. Compiles the plain-language companion PEBBLE.md (pebble.py)
    4. Patches index.html responsive CSS and KaTeX guards (patch_index.py)
    5. Verifies monolithic sync (rewrite.py --check)
    6. Verifies PEBBLE.md sync (pebble.py --check)
    7. Verifies index.html invariants (patch_index.py --check)
    8. Verifies formatting (wrap.py --check)
    9. Runs the full pytest test suite
    10. Optionally builds the Lean 4 formal model (-WithMath)

    Flags are optional bypasses.

.PARAMETER CheckOnly
    Skip formatting and compilation; only verify sync, format, HTML, and tests.

.PARAMETER SkipTests
    Skip running pytest.

.PARAMETER SkipFormat
    Skip the in-place formatting step.

.PARAMETER WithMath
    Also run `lake build` in `math/`.
#>
[CmdletBinding()]
param(
    [switch]$CheckOnly,
    [switch]$SkipTests,
    [switch]$SkipFormat,
    [switch]$WithMath,
    [switch]$NoPause
)

$ErrorActionPreference = "Stop"

if ($CheckOnly -and $SkipFormat) {
    Write-Warning "Both -CheckOnly and -SkipFormat were specified: -CheckOnly already skips formatting. Verification may fail if files are unformatted."
}

$totalSteps = 0
if (-not $CheckOnly -and -not $SkipFormat) { $totalSteps++ }
if (-not $CheckOnly) { $totalSteps += 3 } # rewrite.py, pebble.py, patch_index.py
$totalSteps += 4  # rewrite --check, pebble --check, patch_index --check, wrap --check
if (-not $SkipTests) { $totalSteps++ }
if ($WithMath) { $totalSteps++ }

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

# 3. Compile PEBBLE companion
if (-not $CheckOnly) {
    $step++
    Write-Host "`n[$step/$totalSteps] Compiling plain-language companion (pebble.py)..." -ForegroundColor Yellow
    python pebble.py
    if ($LASTEXITCODE -ne 0) {
        Write-Error "pebble.py compilation failed."
        exit 1
    }
}

# 4. Patch index.html
if (-not $CheckOnly) {
    $step++
    Write-Host "`n[$step/$totalSteps] Patching index.html invariants (patch_index.py)..." -ForegroundColor Yellow
    python patch_index.py
    if ($LASTEXITCODE -ne 0) {
        Write-Error "patch_index.py failed."
        exit 1
    }
}

# 5. Verify monolithic sync
$step++
Write-Host "`n[$step/$totalSteps] Verifying monolithic document sync (rewrite.py --check)..." -ForegroundColor Yellow
python rewrite.py --check
if ($LASTEXITCODE -ne 0) {
    Write-Error "rewrite.py --check failed: monolithic document is out of sync."
    exit 1
}

# 6. Verify PEBBLE sync
$step++
Write-Host "`n[$step/$totalSteps] Verifying PEBBLE.md sync (pebble.py --check)..." -ForegroundColor Yellow
python pebble.py --check
if ($LASTEXITCODE -ne 0) {
    Write-Error "pebble.py --check failed: PEBBLE.md is out of sync."
    exit 1
}

# 7. Verify index.html invariants
$step++
Write-Host "`n[$step/$totalSteps] Verifying index.html invariants (patch_index.py --check)..." -ForegroundColor Yellow
python patch_index.py --check
if ($LASTEXITCODE -ne 0) {
    Write-Error "patch_index.py --check failed: index.html invariants violated."
    exit 1
}

# 8. Verify formatting
$step++
Write-Host "`n[$step/$totalSteps] Verifying formatting (wrap.py --check)..." -ForegroundColor Yellow
python wrap.py --check
if ($LASTEXITCODE -ne 0) {
    Write-Error "wrap.py --check failed: unformatted files detected."
    exit 1
}

# 9. Run test suite
if (-not $SkipTests) {
    $step++
    Write-Host "`n[$step/$totalSteps] Running test suite (pytest)..." -ForegroundColor Yellow
    python -m pytest tests/ -v
    if ($LASTEXITCODE -ne 0) {
        Write-Error "pytest test suite failed."
        exit 1
    }
}

# 10. Optional Lean 4 formal model build
if ($WithMath) {
    $step++
    Write-Host "`n[$step/$totalSteps] Building Lean 4 formal model (lake build)..." -ForegroundColor Yellow
    Push-Location math
    try {
        lake build
        if ($LASTEXITCODE -ne 0) {
            Write-Error "lake build failed."
            exit 1
        }
    } finally {
        Pop-Location
    }
}

Write-Host "`n==================================================" -ForegroundColor Green
Write-Host " Build succeeded! All artifacts up to date and verified." -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

if (-not $NoPause) {
    Write-Host "`nPress [Enter] to exit..." -NoNewline
    try {
        while ($true) {
            $key = [System.Console]::ReadKey($true)
            if ($key.Key -eq [System.ConsoleKey]::Enter) {
                break
            }
        }
        Write-Host ""
    } catch {
        [void](Read-Host)
    }
}
exit 0
