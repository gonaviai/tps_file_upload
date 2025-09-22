@echo off
title Manual Installation Steps
echo.
echo ===================================================
echo         MANUAL INSTALLATION GUIDE
echo ===================================================
echo.
echo If the automatic installer crashed, follow these steps manually:
echo.
echo 1. INSTALL PYTHON (if not already installed):
echo    - Go to https://python.org/downloads/
echo    - Download Python 3.8 or newer
echo    - During installation, CHECK "Add Python to PATH"
echo    - Restart your computer after installation
echo.
echo 2. OPEN COMMAND PROMPT:
echo    - Press Windows Key + R
echo    - Type: cmd
echo    - Press Enter
echo.
echo 3. NAVIGATE TO THIS FOLDER:
echo    - Type: cd "%cd%"
echo    - Press Enter
echo.
echo 4. RUN THESE COMMANDS ONE BY ONE:
echo.
echo    python --version
echo    python -m pip install --upgrade pip
echo    python -m pip install -r requirements.txt
echo    python build_executable.py
echo    python create_shortcut.py
echo.
echo 5. ALTERNATIVE PYTHON COMMANDS (if python doesn't work):
echo    - Try "py" instead of "python"
echo    - Try "python3" instead of "python"
echo.
echo 6. IF PIP INSTALLATION FAILS:
echo    - Try: python -m pip install --user -r requirements.txt
echo    - Or: python -m pip install boto3 pyinstaller pillow pywin32
echo.
echo 7. FIND YOUR EXECUTABLE:
echo    - After successful build: dist\navi_uploader.exe
echo    - Double-click to run the uploader
echo.
echo ===================================================
pause
