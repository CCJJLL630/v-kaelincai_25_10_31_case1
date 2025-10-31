# PowerShell setup script for Project A - Faulty Implementation
$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "Setting up Python environment for Project A (Faulty)..." -ForegroundColor Cyan

# Create virtual environment
python -m venv "$ScriptDir\.venv"

# Activate and install dependencies
& "$ScriptDir\.venv\Scripts\Activate.ps1"
python -m pip install --upgrade pip
pip install -r "$ScriptDir\requirements_original.txt"

Write-Host "Environment ready in $ScriptDir\.venv" -ForegroundColor Green
