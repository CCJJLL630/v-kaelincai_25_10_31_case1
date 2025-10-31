# PowerShell execution script for Project A - Faulty Implementation
$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$LogFile = Join-Path $ScriptDir "log_original.txt"
$TimeFile = Join-Path $ScriptDir "time_original.txt"

Write-Host "Running Project A (Faulty) tests..." -ForegroundColor Cyan

# Activate virtual environment if it exists
if (Test-Path "$ScriptDir\.venv\Scripts\Activate.ps1") {
    & "$ScriptDir\.venv\Scripts\Activate.ps1"
}

# Measure execution time
$StartTime = Get-Date

# Run tests and capture output (allow failures)
$OriginalErrorActionPreference = $ErrorActionPreference
$ErrorActionPreference = "Continue"
pytest "$ScriptDir\test_original.py" --maxfail=1 --disable-warnings -q *>&1 | Tee-Object -FilePath $LogFile
$ExitStatus = $LASTEXITCODE
$ErrorActionPreference = $OriginalErrorActionPreference

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
