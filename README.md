# Navi File Uploader

A robust, efficient Windows desktop application for uploading files to AWS S3 with smart duplicate detection and security-focused design.

## 🚀 Quick Start

1. **Easy Installation**: Double-click `install.bat` and wait for completion
2. **Desktop Shortcut**: Look for "Navi_upload" on your desktop  
3. **Configure**: Enter your AWS credentials and upload directory
4. **Upload**: Click "Start Upload" and watch the progress!

## ✨ Key Features

### 🔒 **Security First**
- **Upload-only permissions**: Cannot download or access existing files
- **Minimal AWS IAM policy**: Only `s3:PutObject` and `s3:ListBucket`
- **Local credential storage**: AWS keys stored securely on your machine
- **Privacy protection**: Progress shows percentages, not filenames

### ⚡ **High Performance**
- **Smart duplicate detection**: Only uploads files missing from S3
- **Multi-threaded uploads**: Multiple files uploaded simultaneously
- **Large file optimization**: Automatic multipart upload for big files
- **Robust error handling**: Continues even if individual files fail

### 🎯 **User-Friendly**
- **No installation required**: Self-contained executable
- **Simple GUI**: Easy configuration and one-click uploading
- **Real-time progress**: Visual progress bar with percentage completion
- **Desktop integration**: Custom icon and shortcut

## 📁 Project Structure

```
navi_file_upload/
├── 📱 navi_uploader.py          # Main application with GUI
├── 🔧 build_executable.py       # Creates Windows .exe file
├── 🔗 create_shortcut.py        # Generates desktop shortcut
├── ⚙️  install.bat              # One-click Windows installer
├── 📦 requirements.txt          # Python dependencies
├── 🎨 Navi_logo.jpg            # Application icon
├── 📖 SETUP_INSTRUCTIONS.md     # Detailed setup guide
├── 📋 uploader_config.json      # User configuration (created after first run)
├── 📝 navi_uploader.log         # Upload activity log
└── 📊 README.md                # This file
```

## 🛠️ Technical Specifications

### **Core Components**
- **Backend**: Python 3.8+ with boto3 for AWS integration
- **GUI**: Tkinter for cross-platform desktop interface  
- **Packaging**: PyInstaller for standalone executable creation
- **Threading**: Concurrent uploads for maximum efficiency

### **AWS Integration**
- Uses minimal IAM permissions for security
- Supports all AWS regions
- Handles multipart uploads automatically
- Efficient S3 object listing for duplicate detection

### **File Management** 
- Recursive directory scanning
- Path normalization for cross-platform compatibility
- Smart file comparison using S3 object keys
- Upload progress tracking by total data size

## 📊 Performance Metrics

- **Upload Speed**: Multi-threaded for maximum throughput
- **Memory Usage**: Efficient streaming for large files
- **CPU Usage**: Optimized with configurable worker threads
- **Network Efficiency**: Only uploads changed/new files

## 🔧 Configuration Options

Edit `uploader_config.json` to customize:
```json
{
    "max_workers": 5,           // Simultaneous uploads
    "chunk_size": 8388608,      // 8MB chunks for multipart
    "aws_region": "us-east-1",  // Your preferred AWS region
    "upload_directory": "...",   // Local folder to upload
    "bucket_name": "...",       // Your S3 bucket name
}
```

## 🆘 Troubleshooting

### Common Issues
- **Connection Failed**: Check AWS credentials and bucket name
- **Slow Uploads**: Verify internet connection and increase `max_workers`
- **Permission Denied**: Ensure IAM policy includes required S3 actions
- **Large File Errors**: Multipart upload handles files up to 5TB

### Log Files
Check `navi_uploader.log` for detailed error messages and upload history.

## 🏗️ Development

### **Requirements**
- Python 3.8+
- boto3 for AWS S3 integration
- PyInstaller for executable creation  
- Pillow for icon processing
- pywin32 for Windows shortcuts

### **Building from Source**
```bash
pip install -r requirements.txt
python build_executable.py
python create_shortcut.py
```

## 📄 License & Usage

Built for efficient, secure file uploads to AWS S3. Designed for enterprise use with security and performance in mind.

---

**🔥 Ready to upload? Double-click that "Navi_upload" shortcut and get started!**