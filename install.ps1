# Navi File Uploader - PowerShell Installer
# Run this if the .bat files don't work

Write-Host ""
Write-Host "===================================================" -ForegroundColor Green
Write-Host "       NAVI FILE UPLOADER - POWERSHELL INSTALLER" -ForegroundColor Green  
Write-Host "===================================================" -ForegroundColor Green
Write-Host ""

# Check execution policy
$executionPolicy = Get-ExecutionPolicy
if ($executionPolicy -eq "Restricted") {
    Write-Host "❌ PowerShell execution policy is restricted" -ForegroundColor Red
    Write-Host "Run this command as Administrator first:" -ForegroundColor Yellow
    Write-Host "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if we're in the right directory
if (-not (Test-Path "navi_uploader.py")) {
    Write-Host "❌ navi_uploader.py not found in current directory" -ForegroundColor Red
    Write-Host "Please run this script from the correct folder" -ForegroundColor Yellow
    Write-Host "Current directory: $(Get-Location)" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Test Python installation
Write-Host "[1/5] Checking Python installation..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
        $pythonCmd = "python"
    } else {
        $pythonVersion = py --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
            $pythonCmd = "py"
        } else {
            throw "Python not found"
        }
    }
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python from https://python.org" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check pip
Write-Host "[2/5] Checking pip..." -ForegroundColor Cyan
try {
    & $pythonCmd -m pip --version | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ pip found" -ForegroundColor Green
    } else {
        throw "pip not found"
    }
} catch {
    Write-Host "❌ pip is not available" -ForegroundColor Red
    Write-Host "Please reinstall Python with pip included" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Upgrade pip
Write-Host "[3/5] Upgrading pip..." -ForegroundColor Cyan
try {
    & $pythonCmd -m pip install --upgrade pip --quiet
    Write-Host "✅ pip upgraded" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Could not upgrade pip, continuing..." -ForegroundColor Yellow
}

# Install requirements
Write-Host "[4/5] Installing dependencies..." -ForegroundColor Cyan
Write-Host "This may take a few minutes..." -ForegroundColor Yellow
try {
    & $pythonCmd -m pip install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Dependencies installed" -ForegroundColor Green
    } else {
        throw "Failed to install dependencies"
    }
} catch {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    Write-Host ""
    Write-Host "Try running as Administrator or check your internet connection" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Build executable
Write-Host "[5/5] Building executable..." -ForegroundColor Cyan
Write-Host "This may take several minutes..." -ForegroundColor Yellow
try {
    & $pythonCmd build_executable.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Executable built successfully" -ForegroundColor Green
    } else {
        throw "Failed to build executable"
    }
} catch {
    Write-Host "❌ Failed to build executable" -ForegroundColor Red
    Write-Host "Check the error messages above" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Create shortcut
Write-Host "[6/6] Creating desktop shortcut..." -ForegroundColor Cyan
try {
    & $pythonCmd create_shortcut.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Desktop shortcut created" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Could not create desktop shortcut" -ForegroundColor Yellow
        Write-Host "You can run manually: dist\navi_uploader.exe" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️ Could not create desktop shortcut" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "===================================================" -ForegroundColor Green
Write-Host "              INSTALLATION COMPLETE!" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Green
Write-Host ""
Write-Host "✅ Navi File Uploader is ready to use" -ForegroundColor Green
Write-Host "📁 Executable: $(Get-Location)\dist\navi_uploader.exe" -ForegroundColor Cyan
Write-Host "🖥️ Look for 'Navi_upload' shortcut on your desktop" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Double-click the desktop shortcut"
Write-Host "2. Configure your AWS credentials"
Write-Host "3. Select upload directory and start uploading!"
Write-Host ""
Read-Host "Press Enter to exit"
