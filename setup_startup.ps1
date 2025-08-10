# PowerShell script to add Alumni DBMS to Windows startup
# Run this script as Administrator

Write-Host "Setting up Alumni DBMS to start automatically with Windows..." -ForegroundColor Green
Write-Host ""

# Get the current directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$startupScript = Join-Path $scriptPath "startup_script.bat"

# Create the startup registry entry
$startupPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
$startupName = "AlumniDBMS"

try {
    # Check if the startup entry already exists
    $existing = Get-ItemProperty -Path $startupPath -Name $startupName -ErrorAction SilentlyContinue
    
    if ($existing) {
        Write-Host "Startup entry already exists. Updating..." -ForegroundColor Yellow
        Set-ItemProperty -Path $startupPath -Name $startupName -Value "`"$startupScript`""
    } else {
        Write-Host "Creating new startup entry..." -ForegroundColor Yellow
        New-ItemProperty -Path $startupPath -Name $startupName -Value "`"$startupScript`"" -PropertyType String
    }
    
    Write-Host "✅ Successfully added Alumni DBMS to Windows startup!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your application will now start automatically when Windows starts." -ForegroundColor Cyan
    Write-Host "To test it now, you can run: startup_script.bat" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "To remove from startup later, run this command:" -ForegroundColor Yellow
    Write-Host "Remove-ItemProperty -Path '$startupPath' -Name '$startupName'" -ForegroundColor White
    
} catch {
    Write-Host "❌ Error setting up startup: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Try running this script as Administrator." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
