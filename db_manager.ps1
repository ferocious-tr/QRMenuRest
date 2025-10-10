# Database Management Menu
# Main menu for all database operations

function Show-Header {
    Write-Host ""
    Write-Host ("=" * 60) -ForegroundColor Cyan
    Write-Host "DATABASE MANAGEMENT UTILITY" -ForegroundColor Yellow
    Write-Host ("=" * 60) -ForegroundColor Cyan
    Write-Host ""
}

function Show-Menu {
    Write-Host "What would you like to do?" -ForegroundColor White
    Write-Host ""
    Write-Host "  1. " -NoNewline -ForegroundColor Yellow
    Write-Host "🗑️  Reset Database (Simple)" -ForegroundColor White
    Write-Host "     Delete all data and start fresh" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  2. " -NoNewline -ForegroundColor Cyan
    Write-Host "🔧 Reset Database (Advanced)" -ForegroundColor White
    Write-Host "     Selective reset with options" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  3. " -NoNewline -ForegroundColor Green
    Write-Host "➕ Add Sample Data" -ForegroundColor White
    Write-Host "     Create test data for development" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  4. " -NoNewline -ForegroundColor Magenta
    Write-Host "🔄 Full Reset + Sample Data" -ForegroundColor White
    Write-Host "     Reset everything and add test data" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  5. " -NoNewline -ForegroundColor Red
    Write-Host "❌ Exit" -ForegroundColor White
    Write-Host ""
    Write-Host ("=" * 60) -ForegroundColor Cyan
    Write-Host ""
}

function Reset-And-Sample {
    Write-Host "`n🔄 Full Reset + Sample Data Operation" -ForegroundColor Magenta
    Write-Host ""
    Write-Host "This will:" -ForegroundColor Yellow
    Write-Host "  1. Delete all existing data" -ForegroundColor Gray
    Write-Host "  2. Create backup" -ForegroundColor Gray
    Write-Host "  3. Add fresh sample data" -ForegroundColor Gray
    Write-Host ""
    
    $confirm = Read-Host "Continue? Type 'YES' to confirm"
    
    if ($confirm -ne "YES") {
        Write-Host "`n❌ Operation cancelled." -ForegroundColor Red
        return
    }
    
    Write-Host "`nStep 1/2: Resetting database..." -ForegroundColor Yellow
    Write-Host "YES" | python reset_database.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`nStep 2/2: Adding sample data..." -ForegroundColor Yellow
        Write-Host "YES" | python add_sample_data.py
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "`n✅ Full reset completed successfully!" -ForegroundColor Green
            Write-Host "   You can now run: streamlit run app.py" -ForegroundColor Cyan
        }
    }
}

function Main {
    Clear-Host
    Show-Header
    
    # Check if Python is available
    try {
        $pythonVersion = python --version 2>&1
        Write-Host "Python detected: $pythonVersion" -ForegroundColor Green
        Write-Host ""
    } catch {
        Write-Host "❌ Error: Python not found!" -ForegroundColor Red
        Write-Host "Please install Python and try again." -ForegroundColor Yellow
        Write-Host ""
        Pause
        exit
    }
    
    Show-Menu
    
    $choice = Read-Host "Select an option (1-5)"
    
    switch ($choice) {
        "1" {
            Write-Host "`n🗑️  Starting simple reset..." -ForegroundColor Yellow
            python reset_database.py
        }
        "2" {
            Write-Host "`n🔧 Starting advanced reset..." -ForegroundColor Cyan
            python reset_database_advanced.py
        }
        "3" {
            Write-Host "`n➕ Adding sample data..." -ForegroundColor Green
            python add_sample_data.py
        }
        "4" {
            Reset-And-Sample
        }
        "5" {
            Write-Host "`n❌ Exiting..." -ForegroundColor Red
            exit
        }
        default {
            Write-Host "`n❌ Invalid option!" -ForegroundColor Red
        }
    }
    
    Write-Host ""
    Write-Host ("=" * 60) -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Press any key to continue..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

# Run main function
Main
