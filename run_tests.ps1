#!/usr/bin/env pwsh
# run_tests.ps1 - One-click test execution script for fake-useragent

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "fake-useragent Test Suite" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get the script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "Running tests..." -ForegroundColor Yellow
Write-Host ""

# Run the test suite
python test_fake_useragent.py

# Capture exit code
$exitCode = $LASTEXITCODE

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
if ($exitCode -eq 0) {
    Write-Host "All tests passed! ✓" -ForegroundColor Green
} else {
    Write-Host "Some tests failed! ✗" -ForegroundColor Red
}
Write-Host "========================================" -ForegroundColor Cyan

exit $exitCode
