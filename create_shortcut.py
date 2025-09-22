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
    
    # Paths - use batch file for better compatibility
    bat_path = Path.cwd() / "run_navi_uploader.bat"
    exe_path = Path.cwd() / "dist" / "navi_uploader.exe"
    shortcut_path = desktop_path / "Navi_upload.lnk"
    icon_path = Path.cwd() / "Navi_logo.jpg"
    
    # Prefer batch file if available, fallback to exe
    target_path = bat_path if bat_path.exists() else exe_path
    
    if not target_path.exists():
        print(f"❌ Neither batch file nor executable found")
        print("Please run the installer or build_executable.py first")
        return False
    
    try:
        # For Windows, we'll create a .lnk shortcut
        if sys.platform == "win32":
            import win32com.client
            
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.Targetpath = str(target_path)
            shortcut.WorkingDirectory = str(Path.cwd())
            shortcut.Description = "Navi File Uploader - Efficient S3 Upload Tool"
            
            # Set icon if available - convert JPG to ICO for Windows compatibility
            if icon_path.exists():
                try:
                    # Convert JPG to ICO format for Windows shortcut
                    from PIL import Image
                    ico_path = Path.cwd() / "navi_icon.ico"
                    
                    img = Image.open(icon_path)
                    # Resize to standard icon sizes for better compatibility
                    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
                    img.save(ico_path, format='ICO', sizes=icon_sizes)
                    
                    shortcut.IconLocation = str(ico_path)
                    print(f"✅ Icon converted and applied: {ico_path}")
                    
                except ImportError:
                    print("⚠️ PIL not available for icon conversion")
                    # Fallback: try to use system default
                    shortcut.IconLocation = "shell32.dll,43"  # Folder icon as fallback
                    
                except Exception as e:
                    print(f"⚠️ Could not set custom icon: {e}")
                    # Use system default folder icon
                    shortcut.IconLocation = "shell32.dll,43"
            
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
    bat_file = Path.cwd() / "run_navi_uploader.bat"
    
    # If our batch file exists, just copy it to desktop
    if bat_file.exists():
        desktop_path = Path.home() / "Desktop"
        if not desktop_path.exists():
            desktop_path = Path.home() / "OneDrive" / "Desktop"
        
        desktop_bat = desktop_path / "Navi_upload.bat"
        
        try:
            import shutil
            shutil.copy2(bat_file, desktop_bat)
            print(f"✅ Batch launcher copied to desktop: {desktop_bat}")
            return True
        except Exception as e:
            print(f"❌ Error copying batch launcher: {e}")
            return False
    
    print("❌ run_navi_uploader.bat not found")
    return False

if __name__ == "__main__":
    print("🔗 Creating Desktop Shortcut")
    print("=" * 30)
    
    success = create_desktop_shortcut()
    if not success:
        print("Trying fallback batch launcher...")
        create_batch_launcher()
