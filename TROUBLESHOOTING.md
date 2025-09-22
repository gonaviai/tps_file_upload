# 🛠️ Navi File Uploader - Troubleshooting Guide

## ❌ "This version can't run on your PC" Error

This Windows security error can have several causes. Try these solutions:

### 🔧 **Solution 1: Windows SmartScreen Override**
1. Right-click on `navi_uploader.exe`
2. Select **"Properties"**
3. Check **"Unblock"** at the bottom (if present)
4. Click **"OK"**
5. Try running again

### 🔧 **Solution 2: Run as Administrator**
1. Right-click on `navi_uploader.exe`
2. Select **"Run as administrator"**
3. Click **"Yes"** when prompted

### 🔧 **Solution 3: Windows Defender Exception**
1. Open **Windows Defender** (Windows Security)
2. Go to **Virus & threat protection**
3. Click **"Manage settings"** under Virus & threat protection settings
4. Click **"Add or remove exclusions"**
5. Add the folder containing `navi_uploader.exe`

### 🔧 **Solution 4: Use Direct Python Script (RECOMMENDED)**
Instead of the executable, use the direct Python script:

1. **Double-click `run_navi_uploader.bat`** (this bypasses executable issues)
2. Or manually run: `python navi_uploader.py`

## 🐛 **Other Common Issues**

### **"Python not found" Error**
**Cause**: Python not in Windows PATH

**Solutions**:
- **Option A**: Reinstall Python from python.org, check "Add to PATH"
- **Option B**: Disable Microsoft Store Python alias:
  - Settings → Apps → App execution aliases → Turn off Python
- **Option C**: Use Windows Store Python (may work)

### **"Module not found" Error**  
**Cause**: Missing Python packages

**Solution**: Run the installer again:
```cmd
install.bat
```

### **"AWS connection failed" Error**
**Cause**: Incorrect AWS credentials or permissions

**Solutions**:
1. **Verify credentials** in the uploader GUI
2. **Test connection** using the "Test Connection" button
3. **Check IAM policy** - ensure it has `s3:PutObject` and `s3:ListBucket`
4. **Verify bucket name** - ensure it exists and you have access

### **"No files found to upload" Error**
**Cause**: Empty or inaccessible upload directory

**Solutions**:
1. **Check directory path** - use the "Browse" button
2. **Verify permissions** - ensure you can read the directory
3. **Check file types** - all file types are supported

### **Slow Upload Speeds**
**Cause**: Network or configuration issues

**Solutions**:
1. **Check internet speed** - run a speed test
2. **Increase workers** - edit `uploader_config.json`, increase `max_workers`
3. **Verify network** - try uploading smaller files first

### **"Access Denied" Errors**
**Cause**: Insufficient permissions

**Solutions**:
1. **AWS IAM**: Verify your IAM policy includes required S3 permissions
2. **Local files**: Run as administrator or check file permissions
3. **S3 bucket**: Verify bucket exists and is accessible

## 🚀 **Alternative Running Methods**

If the executable doesn't work, use these alternatives:

### **Method 1: Batch Script (Easiest)**
```cmd
run_navi_uploader.bat
```

### **Method 2: Direct Python**
```cmd
python navi_uploader.py
```

### **Method 3: Python Module**
```cmd
py -m navi_uploader
```

## 📋 **Getting Help**

If issues persist:

1. **Check logs**: Look at `navi_uploader.log` for detailed errors
2. **Run in console**: Use `python navi_uploader.py --console` for debug output
3. **Verify requirements**: Ensure all packages in `requirements.txt` are installed

## 🔍 **Debug Information**

Run these commands to get system info:

```cmd
python --version
pip list | findstr boto3
pip list | findstr pyinstaller
```

This will show your Python version and installed packages for troubleshooting.

---

**💡 TIP**: The `run_navi_uploader.bat` script is often the most reliable method as it bypasses Windows executable restrictions entirely!
