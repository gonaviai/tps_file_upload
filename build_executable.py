#!/usr/bin/env python3
"""
Build script to create standalone Windows executable for Navi Uploader
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

def create_executable():
    """Create standalone executable using PyInstaller"""
    
    # Check if PyInstaller is available
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Convert JPG logo to ICO format for Windows
    icon_path = None
    if os.path.exists("Navi_logo.jpg"):
        try:
            from PIL import Image
            img = Image.open("Navi_logo.jpg")
            # Resize to standard icon sizes
            icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128)]
            img.save("navi_icon.ico", format='ICO', sizes=icon_sizes)
            icon_path = "navi_icon.ico"
            print("Created Windows icon from logo")
        except ImportError:
            print("PIL not available, using default icon")
        except Exception as e:
            print(f"Error creating icon: {e}")
    
    # PyInstaller command through Python module
    cmd = [
        sys.executable, "-m", "PyInstaller",  # Use current Python to run PyInstaller module
        "--onefile",                          # Single executable file
        "--windowed",                         # No console window
        "--name=navi_uploader",               # Executable name
        "--distpath=dist",                    # Output directory
        "--workpath=build",                   # Build directory
        "--specpath=.",                       # Spec file location
        "--add-data=Navi_logo.jpg;.",         # Include logo file
    ]
    
    # Add icon if available
    if icon_path and os.path.exists(icon_path):
        cmd.extend(["--icon", icon_path])
    
    # Add the main script
    cmd.append("navi_uploader.py")
    
    print("Building executable...")
    print("Command:", " ".join(cmd))
    
    try:
        subprocess.check_call(cmd)
        print("\n✅ Executable created successfully!")
        print("📁 Location: dist/navi_uploader.exe")
        
        # Clean up temporary files
        if icon_path and os.path.exists(icon_path):
            os.remove(icon_path)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error building executable: {e}")
        return False

def create_installer_script():
    """Create batch script for easy setup"""
    installer_content = '''@echo off
echo Installing Navi File Uploader...
echo.

REM Install Python requirements
echo Installing Python dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

REM Build executable
echo Building executable...
python build_executable.py

REM Create desktop shortcut
echo Creating desktop shortcut...
python create_shortcut.py

echo.
echo ✅ Installation complete!
echo You can now find "Navi_upload" shortcut on your desktop
echo.
pause
'''
    
    with open("install.bat", "w") as f:
        f.write(installer_content)
    
    print("Created install.bat script")

if __name__ == "__main__":
    print("🚀 Navi Uploader Build Script")
    print("=" * 40)
    
    success = create_executable()
    if success:
        create_installer_script()
        print("\n📋 Next steps:")
        print("1. Run 'install.bat' on Windows to build everything")
        print("2. Or run 'python build_executable.py' directly")
        print("3. The executable will be in the 'dist' folder")
    else:
        print("\n❌ Build failed. Please check the errors above.")
