# Database Reset PowerShell Script
# Quick access script for Windows users

Write-Host ""
Write-Host "=" -NoNewline; Write-Host ("=" * 59)
Write-Host "DATABASE RESET UTILITY"
Write-Host "=" -NoNewline; Write-Host ("=" * 59)
Write-Host ""
Write-Host "1. Simple Reset (All data)" -ForegroundColor Yellow
Write-Host "2. Advanced Reset (Selective)" -ForegroundColor Cyan
Write-Host "3. Exit" -ForegroundColor Red
Write-Host ""
Write-Host "=" -NoNewline; Write-Host ("=" * 59)
Write-Host ""

$choice = Read-Host "Select an option (1-3)"

switch ($choice) {
    "1" {
        Write-Host "`nStarting simple reset..." -ForegroundColor Yellow
        python reset_database.py
    }
    "2" {
        Write-Host "`nStarting advanced reset..." -ForegroundColor Cyan
        python reset_database_advanced.py
    }
    "3" {
        Write-Host "`nExiting..." -ForegroundColor Red
        exit
    }
    default {
        Write-Host "`nInvalid option!" -ForegroundColor Red
        exit
    }
}

Write-Host "`nPress any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
