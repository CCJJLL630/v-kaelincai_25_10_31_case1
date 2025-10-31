# PowerShell execution script for Project B - Optimized Implementation
$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$LogFile = Join-Path $ScriptDir "log_optimized.txt"
$TimeFile = Join-Path $ScriptDir "time_optimized.txt"

Write-Host "Running Project B (Optimized) tests..." -ForegroundColor Cyan

# Activate virtual environment if it exists
if (Test-Path "$ScriptDir\.venv\Scripts\Activate.ps1") {
    & "$ScriptDir\.venv\Scripts\Activate.ps1"
}

# Measure execution time
$StartTime = Get-Date

# Run tests and capture output
pytest "$ScriptDir\test_optimized.py" --disable-warnings -q *>&1 | Tee-Object -FilePath $LogFile
$ExitStatus = $LASTEXITCODE

$EndTime = Get-Date
$Elapsed = ($EndTime - $StartTime).TotalSeconds

# Write performance report
@"
status=$ExitStatus
elapsed_seconds=$([math]::Round($Elapsed, 6))
timestamp=$($EndTime.ToString("o"))
"@ | Set-Content -Path $TimeFile

Write-Host "Results saved to $LogFile and $TimeFile" -ForegroundColor Green
exit $ExitStatus
