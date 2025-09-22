@echo off
title Navi File Uploader - Installation
color 0A

echo.
echo ===================================================
echo         NAVI FILE UPLOADER - INSTALLER
echo ===================================================
echo.

REM Find Python executable
echo [1/5] Finding Python installation...
set PYTHON_CMD=
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    echo ✅ Python found: python
    goto :python_found
)

python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python3
    echo ✅ Python found: python3
    goto :python_found
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    echo ✅ Python found: py
    goto :python_found
)

echo ❌ Python not found in PATH
echo.
echo Please fix one of these issues:
echo 1. Install Python from https://python.org (check "Add to PATH")
echo 2. OR disable Microsoft Store Python alias:
echo    Settings ^> Manage App Execution Aliases ^> Turn off Python
echo 3. OR add Python to your PATH manually
echo.
pause
exit /b 1

:python_found

REM Upgrade pip
echo [2/5] Upgrading pip...
%PYTHON_CMD% -m pip install --upgrade pip --quiet
if %errorlevel% neq 0 (
    echo ⚠️  Warning: Could not upgrade pip (continuing anyway)
) else (
    echo ✅ pip upgraded
)

REM Install requirements
echo [3/5] Installing Python dependencies...
echo This may take a few minutes...
%PYTHON_CMD% -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)
echo ✅ Dependencies installed

REM Build executable
echo [4/5] Building Windows executable...
%PYTHON_CMD% build_executable.py
if %errorlevel% neq 0 (
    echo ❌ Failed to build executable
    echo Please check the error messages above
    pause
    exit /b 1
)

REM Create desktop shortcut
echo [5/5] Creating desktop shortcut...
%PYTHON_CMD% create_shortcut.py
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
