<#
.SYNOPSIS
    Full build pipeline for GMRTI.

.DESCRIPTION
    When run bare (without flags), builds everything:
    1. Formats all markdown and YAML files (wrap.py)
    2. Recompiles the monolithic document and archives prior revisions (rewrite.py)
    3. Compiles the plain-language companion PEBBLE.md (pebble.py)
    4. Compiles index.html via mdd
    5. Verifies monolithic sync (rewrite.py --check)
    6. Verifies PEBBLE.md sync (pebble.py --check)
    7. Verifies index.html invariants (mdd output)
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

.PARAMETER Fast
    Run only non-browser pytest tests (`-m "not browser"`).

.PARAMETER WithMath
    Also run `lake build` in `math/`.

.PARAMETER Python
    Path to the Python executable (defaults to `.venv\Scripts\python.exe` if present, else `python`).
#>
[CmdletBinding()]
param(
    [switch]$CheckOnly,
    [switch]$SkipTests,
    [switch]$SkipFormat,
    [switch]$Fast,
    [switch]$WithMath,
    [switch]$NoPause,
    [string]$Python = ""
)

$ErrorActionPreference = "Stop"

if (-not $Python) {
    $venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
    $Python = if (Test-Path $venvPython) { $venvPython } else { "python" }
}

if ($CheckOnly -and $SkipFormat) {
    Write-Warning "Both -CheckOnly and -SkipFormat were specified: -CheckOnly already skips formatting. Verification may fail if files are unformatted."
}

$totalSteps = 0
if (-not $CheckOnly -and -not $SkipFormat) { $totalSteps++ }
if (-not $CheckOnly) { $totalSteps += 3 } # rewrite.py, pebble.py, mdd -> index.html
$totalSteps += 3 # rewrite --check, pebble --check, wrap --check
if (-not $SkipTests) { $totalSteps++ }
if ($WithMath) { $totalSteps++ }

$script:step = 0

function Invoke-Step {
    param(
        [string]$Label,
        [string]$ErrorMessage,
        [scriptblock]$Action
    )
    $script:step++
    Write-Host "`n[$script:step/$totalSteps] $Label" -ForegroundColor Yellow
    & $Action
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: $ErrorMessage" -ForegroundColor Red
        exit 1
    }
}

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " GMRTI Build Pipeline (Python: $Python)" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

if (-not $CheckOnly -and -not $SkipFormat) {
    Invoke-Step "Formatting files (wrap.py)..." "wrap.py formatting failed." {
        & $Python wrap.py
    }
}

if (-not $CheckOnly) {
    Invoke-Step "Compiling monolithic treatise (rewrite.py)..." "rewrite.py compilation failed." {
        & $Python rewrite.py
    }
    Invoke-Step "Compiling plain-language companion (pebble.py)..." "pebble.py compilation failed." {
        & $Python pebble.py
    }
    Invoke-Step "Compiling MD++ HTML artifact (mdd -> index.html)..." "mdd compilation failed." {
        $null = & mdd --version
        if ($LASTEXITCODE -ne 0) {
            Write-Host "ERROR: mdd CLI not found on PATH." -ForegroundColor Red
            exit 1
        }
        $monoliths = @(Get-ChildItem -Path $PSScriptRoot -Filter "GMRTI_*.md" | Where-Object { $_.Name -match '^GMRTI_\d+\.md$' })
        if ($monoliths.Count -ne 1) {
            Write-Host "ERROR: Expected exactly 1 root monolith, found $($monoliths.Count)." -ForegroundColor Red
            exit 1
        }
        mdd $monoliths[0].FullName -o (Join-Path $PSScriptRoot "index.html") --single --force
    }
}

Invoke-Step "Verifying monolithic document sync (rewrite.py --check)..." "rewrite.py --check failed: monolithic document is out of sync." {
    & $Python rewrite.py --check
}
Invoke-Step "Verifying PEBBLE.md sync (pebble.py --check)..." "pebble.py --check failed: PEBBLE.md is out of sync." {
    & $Python pebble.py --check
}
Invoke-Step "Verifying formatting (wrap.py --check)..." "wrap.py --check failed: unformatted files detected." {
    & $Python wrap.py --check
}

if (-not $SkipTests) {
    Invoke-Step "Running test suite (pytest)..." "pytest test suite failed." {
        if ($Fast) {
            & $Python -m pytest tests/ -m "not browser" -v
        } else {
            & $Python -m pytest tests/ -v
        }
    }
}

if ($WithMath) {
    Invoke-Step "Building Lean 4 formal model (lake build)..." "lake build failed." {
        Push-Location math
        try {
            lake build
        } finally {
            Pop-Location
        }
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
