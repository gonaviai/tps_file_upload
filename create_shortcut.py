#!/usr/bin/env python3
"""
Create desktop shortcut for Navi Uploader
"""

import os
import sys
from pathlib import Path

def create_desktop_shortcut():
    """Create desktop shortcut for Windows"""
    
    # Get desktop path
    desktop_path = Path.home() / "Desktop"
    if not desktop_path.exists():
        desktop_path = Path.home() / "OneDrive" / "Desktop"  # OneDrive Desktop
        if not desktop_path.exists():
            print("❌ Could not find desktop folder")
            return False
    
    # Paths
    exe_path = Path.cwd() / "dist" / "navi_uploader.exe"
    shortcut_path = desktop_path / "Navi_upload.lnk"
    icon_path = Path.cwd() / "Navi_logo.jpg"
    
    if not exe_path.exists():
        print(f"❌ Executable not found: {exe_path}")
        print("Please run build_executable.py first")
        return False
    
    try:
        # For Windows, we'll create a .lnk shortcut
        if sys.platform == "win32":
            import win32com.client
            
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.Targetpath = str(exe_path)
            shortcut.WorkingDirectory = str(exe_path.parent)
            shortcut.Description = "Navi File Uploader - Efficient S3 Upload Tool"
            
            # Set icon if available
            if icon_path.exists():
                # Try to use the exe's embedded icon
                shortcut.IconLocation = f"{exe_path},0"
            
            shortcut.save()
            print(f"✅ Desktop shortcut created: {shortcut_path}")
            return True
            
        else:
            # For development on non-Windows systems, create a simple launcher script
            launcher_content = f'''#!/bin/bash
cd "{Path.cwd()}"
python navi_uploader.py
'''
            launcher_path = desktop_path / "Navi_upload.sh"
            with open(launcher_path, "w") as f:
                f.write(launcher_content)
            
            # Make executable
            os.chmod(launcher_path, 0o755)
            print(f"✅ Launcher script created: {launcher_path}")
            return True
            
    except ImportError:
        print("❌ win32com not available. Installing...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32"])
            print("Please run this script again after installing pywin32")
            return False
        except Exception as e:
            print(f"❌ Error installing pywin32: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating shortcut: {e}")
        return False

def create_batch_launcher():
    """Create simple batch file launcher as fallback"""
    batch_content = f'''@echo off
title Navi File Uploader
cd /d "{Path.cwd()}"
dist\\navi_uploader.exe
pause
'''
    
    batch_path = Path.home() / "Desktop" / "Navi_upload.bat"
    try:
        with open(batch_path, "w") as f:
            f.write(batch_content)
        print(f"✅ Batch launcher created: {batch_path}")
        return True
    except Exception as e:
        print(f"❌ Error creating batch launcher: {e}")
        return False

if __name__ == "__main__":
    print("🔗 Creating Desktop Shortcut")
    print("=" * 30)
    
    success = create_desktop_shortcut()
    if not success:
        print("Trying fallback batch launcher...")
        create_batch_launcher()
