# Navi File Uploader - Complete Setup Guide

This guide will help you set up the Navi File Uploader for efficient, secure file uploads to AWS S3.

## 📋 Prerequisites

- Python 3.8 or higher installed on Windows machine
- AWS Account with S3 access
- Internet connection

## 🔧 AWS S3 Setup

### Step 1: Create S3 Bucket
1. Go to [AWS S3 Console](https://s3.console.aws.amazon.com/)
2. Click **"Create bucket"**
3. Choose a unique bucket name (e.g., `your-company-file-uploads`)
4. Select your preferred AWS region
5. Keep default settings for **Block Public Access** (recommended for security)
6. Click **"Create bucket"**

### Step 2: Create IAM User with Minimal Permissions
1. Go to [AWS IAM Console](https://console.aws.amazon.com/iam/) → **Users** → **Create User**
2. User name: `file-uploader-user`
3. Select **"Programmatic access"** (for API keys)
4. Create a custom policy with these **minimal security permissions**:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::your-bucket-name",
                "arn:aws:s3:::your-bucket-name/*"
            ]
        }
    ]
}
```

⚠️ **IMPORTANT**: Replace `your-bucket-name` with your actual bucket name!

5. **Save the Access Key ID and Secret Access Key** - you'll need these!

## 🛠️ Installation

### Option 1: Quick Setup (Recommended)
1. Download all files to a folder on your Windows machine
2. Double-click `install.bat`
3. Wait for installation to complete
4. Find **"Navi_upload"** shortcut on your desktop

### Option 2: Manual Setup
1. Open Command Prompt or PowerShell
2. Navigate to the project folder
3. Run these commands:
```bash
pip install -r requirements.txt
python build_executable.py
python create_shortcut.py
```

## 🚀 First Time Configuration

1. Double-click the **"Navi_upload"** desktop shortcut
2. Fill in the configuration:
   - **AWS Access Key ID**: From Step 2 above
   - **AWS Secret Access Key**: From Step 2 above  
   - **S3 Bucket Name**: Your bucket name from Step 1
   - **AWS Region**: Your bucket's region (e.g., `us-east-1`)
   - **Upload Directory**: Choose the folder containing files to upload
3. Click **"Save Configuration"**
4. Click **"Test Connection"** to verify everything works
5. Click **"Start Upload"** to begin!

## 🔒 Security Features

- **Upload Only**: The script can only upload files and list existing files - it cannot download or access file contents
- **Smart Duplicate Detection**: Only uploads files that don't already exist in S3
- **Minimal AWS Permissions**: Uses least-privilege IAM policy
- **Local Configuration**: AWS credentials stored locally in encrypted config file

## 📊 Progress Tracking

- **Percentage-based Progress**: Shows upload progress by total data size
- **No File Names Shown**: For privacy, only shows percentage completion
- **Real-time Updates**: Progress bar updates as files are uploaded

## ⚡ Performance Features

- **Multi-threaded Uploads**: Uploads multiple files simultaneously for speed
- **Smart File Detection**: Only uploads new/changed files
- **Large File Support**: Automatic multipart upload for large files
- **Robust Error Handling**: Continues uploading even if individual files fail

## 🔄 Daily Usage

1. Double-click **"Navi_upload"** on your desktop
2. Click **"Start Upload"**
3. Watch the progress bar - no interaction needed!
4. Get notification when complete

## 🐛 Troubleshooting

### "AWS connection failed"
- Double-check your AWS Access Key ID and Secret Access Key
- Verify the bucket name is correct
- Ensure your IAM user has the required permissions

### "Directory does not exist"
- Make sure the upload directory path is correct
- Use the "Browse" button to select a valid folder

### "No files found to upload"  
- Check that the selected directory contains files
- Verify you have read permissions for the directory

### Slow Upload Speeds
- Check your internet connection
- Large files are automatically optimized with multipart upload
- Multiple small files upload simultaneously

## 📁 File Structure
```
navi_uploader/
├── navi_uploader.py          # Main application
├── requirements.txt          # Python dependencies  
├── build_executable.py       # Creates Windows executable
├── create_shortcut.py        # Creates desktop shortcut
├── install.bat              # One-click installer
├── Navi_logo.jpg            # Logo for shortcut
├── uploader_config.json     # Configuration (created after first run)
└── navi_uploader.log        # Upload log file
```

## 🔧 Advanced Configuration

Edit `uploader_config.json` to customize:
- `max_workers`: Number of simultaneous uploads (default: 5)
- `chunk_size`: Size of upload chunks for large files (default: 8MB)

## 📞 Support

If you encounter issues:
1. Check the `navi_uploader.log` file for detailed error messages
2. Verify your AWS credentials and permissions
3. Ensure your internet connection is stable
4. Try the "Test Connection" button first

---

**Made with ❤️ for efficient, secure file uploads**
