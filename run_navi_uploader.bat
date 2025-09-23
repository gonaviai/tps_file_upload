@echo off
title Navi File Uploader
color 0A

echo.
echo ===================================================
echo         NAVI FILE UPLOADER - DIRECT RUN
echo ===================================================
echo.

REM Find Python executable
set PYTHON_CMD=
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    goto :python_found
)

python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python3
    goto :python_found
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    goto :python_found
)

echo [ERROR] Python not found in PATH
pause
exit /b 1

:python_found

REM Change to script directory
cd /d "%~dp0"

REM Run the uploader directly with Python
echo [START] Starting Navi File Uploader...
%PYTHON_CMD% navi_uploader.py

echo.
echo [OK] Navi File Uploader closed
REM Terminal will close automatically
