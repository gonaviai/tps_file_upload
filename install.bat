@echo off
title Navi File Uploader - Installation
color 0A

echo.
echo ===================================================
echo         NAVI FILE UPLOADER - INSTALLER
echo ===================================================
echo.

REM Check if Python is installed
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)
echo ✅ Python found

REM Check if pip is available
echo [2/5] Checking pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not available
    echo Please reinstall Python with pip included
    pause
    exit /b 1
)
echo ✅ pip found

REM Upgrade pip
echo [3/5] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo ✅ pip upgraded

REM Install requirements
echo [4/5] Installing Python dependencies...
echo This may take a few minutes...
python -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)
echo ✅ Dependencies installed

REM Build executable
echo [5/5] Building Windows executable...
python build_executable.py
if %errorlevel% neq 0 (
    echo ❌ Failed to build executable
    echo Please check the error messages above
    pause
    exit /b 1
)

REM Create desktop shortcut
echo [6/6] Creating desktop shortcut...
python create_shortcut.py
if %errorlevel% neq 0 (
    echo ⚠️  Warning: Could not create desktop shortcut
    echo You can manually run the executable from: dist\navi_uploader.exe
)

echo.
echo ===================================================
echo              INSTALLATION COMPLETE! 
echo ===================================================
echo.
echo ✅ Navi File Uploader is ready to use
echo 📁 Executable location: %cd%\dist\navi_uploader.exe
echo 🖥️  Desktop shortcut: "Navi_upload"
echo.
echo Next steps:
echo 1. Look for "Navi_upload" shortcut on your desktop
echo 2. Double-click to open the uploader
echo 3. Configure your AWS credentials and upload directory
echo 4. Test the connection and start uploading!
echo.
echo For help, see: SETUP_INSTRUCTIONS.md
echo.
pause
