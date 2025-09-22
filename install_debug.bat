@echo off
title Navi File Uploader - Installation (Debug Mode)
color 0F

echo.
echo ===================================================
echo    NAVI FILE UPLOADER - DEBUG INSTALLER
echo ===================================================
echo.

echo Current directory: %cd%
echo.

REM Always pause at the end, even if there's an error
set "PAUSE_AT_END=1"

REM Check if we're in the right directory
if not exist "navi_uploader.py" (
    echo ❌ ERROR: navi_uploader.py not found in current directory
    echo Please make sure you're running this from the correct folder
    echo Expected files: navi_uploader.py, requirements.txt, build_executable.py
    echo.
    dir *.py *.txt 2>nul
    echo.
    pause
    exit /b 1
)

REM Test Python installation with detailed output
echo [1/6] Testing Python installation...
python --version
if %errorlevel% neq 0 (
    echo.
    echo ❌ Python command failed. Trying alternative commands...
    py --version
    if %errorlevel% neq 0 (
        python3 --version
        if %errorlevel% neq 0 (
            echo.
            echo ❌ Python is not installed or not accessible
            echo.
            echo Solutions:
            echo 1. Install Python from https://python.org
            echo 2. During installation, check "Add Python to PATH"
            echo 3. Restart your computer after installation
            echo 4. Or try running this script as Administrator
            echo.
            pause
            exit /b 1
        ) else (
            set PYTHON_CMD=python3
        )
    ) else (
        set PYTHON_CMD=py
    )
) else (
    set PYTHON_CMD=python
)

echo ✅ Python found: %PYTHON_CMD%
echo.

REM Test pip with detailed output
echo [2/6] Testing pip...
%PYTHON_CMD% -m pip --version
if %errorlevel% neq 0 (
    echo ❌ pip module not found
    echo Trying to install pip...
    %PYTHON_CMD% -m ensurepip --upgrade
    if %errorlevel% neq 0 (
        echo ❌ Failed to install pip
        echo Please reinstall Python with pip included
        pause
        exit /b 1
    )
)
echo ✅ pip found
echo.

REM Upgrade pip with visible output
echo [3/6] Upgrading pip...
%PYTHON_CMD% -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo ⚠️  Warning: Could not upgrade pip, continuing anyway...
)
echo ✅ pip upgrade completed
echo.

REM Install requirements with visible output
echo [4/6] Installing Python dependencies...
echo This may take a few minutes, please wait...
echo.
%PYTHON_CMD% -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo ❌ Failed to install dependencies
    echo.
    echo Common solutions:
    echo 1. Check your internet connection
    echo 2. Try running as Administrator
    echo 3. Try: %PYTHON_CMD% -m pip install --user -r requirements.txt
    echo 4. If behind a firewall, try: %PYTHON_CMD% -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
    echo.
    pause
    exit /b 1
)
echo ✅ Dependencies installed successfully
echo.

REM Test if required modules are importable
echo [5/6] Testing installed modules...
%PYTHON_CMD% -c "import boto3; import tkinter; import PyInstaller; print('All required modules imported successfully')"
if %errorlevel% neq 0 (
    echo ❌ Some required modules could not be imported
    echo This might cause issues during executable creation
    echo.
    pause
)
echo ✅ Module test passed
echo.

REM Build executable with visible output
echo [6/6] Building Windows executable...
echo This may take several minutes...
echo.
%PYTHON_CMD% build_executable.py
if %errorlevel% neq 0 (
    echo.
    echo ❌ Failed to build executable
    echo Check the error messages above for details
    echo.
    echo Common solutions:
    echo 1. Make sure all files are in the same directory
    echo 2. Try running as Administrator
    echo 3. Check if antivirus is blocking PyInstaller
    echo.
    pause
    exit /b 1
)

REM Create desktop shortcut
echo.
echo Creating desktop shortcut...
%PYTHON_CMD% create_shortcut.py
if %errorlevel% neq 0 (
    echo ⚠️  Warning: Could not create desktop shortcut
    echo You can manually run: dist\navi_uploader.exe
)

echo.
echo ===================================================
echo              INSTALLATION COMPLETE! 
echo ===================================================
echo.
echo ✅ Navi File Uploader is ready to use
echo 📁 Executable: %cd%\dist\navi_uploader.exe
echo 🖥️  Look for "Navi_upload" shortcut on your desktop
echo.
echo Next steps:
echo 1. Double-click the desktop shortcut (or run dist\navi_uploader.exe)
echo 2. Configure your AWS credentials
echo 3. Select your upload directory
echo 4. Test connection and start uploading!
echo.
pause
