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
    echo [OK] Python found: python
    goto :python_found
)

python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python3
    echo [OK] Python found: python3
    goto :python_found
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    echo [OK] Python found: py
    goto :python_found
)

echo [ERROR] Python not found in PATH
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
    echo [WARNING] Could not upgrade pip (continuing anyway)
) else (
    echo [OK] pip upgraded
)

REM Install requirements
echo [3/5] Installing Python dependencies...
echo This may take a few minutes...
%PYTHON_CMD% -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)
echo [OK] Dependencies installed

REM Create desktop shortcut
echo [4/4] Creating desktop shortcut...
%PYTHON_CMD% create_shortcut.py
if %errorlevel% neq 0 (
    echo [WARNING] Could not create desktop shortcut
    echo You can manually run: run_navi_uploader.bat
)

echo.
echo ===================================================
echo              INSTALLATION COMPLETE! 
echo ===================================================
echo.
echo [OK] Navi File Uploader is ready to use
echo [FILE] Launcher location: %cd%\run_navi_uploader.bat
echo [SHORTCUT] Desktop shortcut: "Navi Upload"
echo.
echo Next steps:
echo 1. Look for "Navi Upload" shortcut on your desktop
echo 2. Double-click to open the uploader
echo 3. Enter your server credentials (first time only)
echo 4. Upload will start automatically!
echo.
echo Alternative: You can also run "run_navi_uploader.bat" directly
echo.
echo For help, see: SETUP_INSTRUCTIONS.md
echo.
pause
