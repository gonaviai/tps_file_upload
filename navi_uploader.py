#!/usr/bin/env python3
"""
Navi File Uploader - Efficient S3 Upload Script
Uploads files to AWS S3 bucket with smart duplicate detection
"""

import os
import sys
import json
import hashlib
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Set, Tuple
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('navi_uploader.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class NaviUploader:
    def __init__(self):
        self.config_file = 'uploader_config.json'
        self.config = self.load_config()
        self.s3_client = None
        self.upload_stats = {
            'total_files': 0,
            'total_size': 0,
            'uploaded_files': 0,
            'uploaded_size': 0,
            'skipped_files': 0
        }
        
    def load_config(self) -> Dict:
        """Load configuration from JSON file or create default"""
        default_config = {
            'aws_access_key_id': '',
            'aws_secret_access_key': '',
            'bucket_name': 'tps-files-from-uploader',
            'aws_region': 'us-west-1',
            'upload_directory': 'C:/Users/vivek/Downloads',
            'max_workers': 5,
            'chunk_size': 8 * 1024 * 1024  # 8MB chunks for multipart upload
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    default_config.update(config)
                    return default_config
            except Exception as e:
                logger.error("Error loading config: %s", e)
                return default_config
        else:
            self.save_config(default_config)
            return default_config
    
    def save_config(self, config: Dict):
        """Save configuration to JSON file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            logger.error("Error saving config: %s", e)
    
    def setup_aws_client(self) -> bool:
        """Initialize AWS S3 client with credentials"""
        try:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=self.config['aws_access_key_id'],
                aws_secret_access_key=self.config['aws_secret_access_key'],
                region_name=self.config['aws_region']
            )
            
            # Test connection
            self.s3_client.head_bucket(Bucket=self.config['bucket_name'])
            logger.info("AWS S3 connection established successfully")
            return True
            
        except NoCredentialsError:
            logger.error("AWS credentials not found")
            return False
        except ClientError as e:
            logger.error("AWS connection failed: %s", e)
            return False
        except Exception as e:
            logger.error("Unexpected error setting up AWS: %s", e)
            return False
    
    def get_s3_file_list(self) -> Set[str]:
        """Get list of existing files in S3 bucket (keys only for security)"""
        try:
            existing_files = set()
            paginator = self.s3_client.get_paginator('list_objects_v2')
            
            for page in paginator.paginate(Bucket=self.config['bucket_name']):
                if 'Contents' in page:
                    for obj in page['Contents']:
                        existing_files.add(obj['Key'])
            
            logger.info("Found %d existing files in S3 bucket", len(existing_files))
            return existing_files
            
        except Exception as e:
            logger.error("Error listing S3 files: %s", e)
            return set()
    
    def calculate_file_hash(self, file_path: str) -> str:
        """Calculate MD5 hash of file for comparison"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logger.error("Error calculating hash for %s: %s", file_path, e)
            return ""
    
    def get_local_files(self, directory: str) -> List[Tuple[str, str, int]]:
        """Get list of local files with their paths, relative paths, and sizes"""
        local_files = []
        directory_path = Path(directory)
        
        if not directory_path.exists():
            logger.error("Directory does not exist: %s", directory)
            return local_files
        
        try:
            for file_path in directory_path.rglob('*'):
                if file_path.is_file():
                    relative_path = str(file_path.relative_to(directory_path)).replace('\\', '/')
                    size = file_path.stat().st_size
                    local_files.append((str(file_path), relative_path, size))
            
            logger.info("Found %d local files", len(local_files))
            return local_files
            
        except Exception as e:
            logger.error("Error scanning local directory: %s", e)
            return []
    
    def upload_file(self, file_path: str, s3_key: str, file_size: int) -> bool:
        """Upload a single file to S3"""
        try:
            # For large files, use multipart upload
            if file_size > self.config['chunk_size']:
                self.s3_client.upload_file(
                    file_path, 
                    self.config['bucket_name'], 
                    s3_key,
                    Config=boto3.s3.transfer.TransferConfig(
                        multipart_threshold=self.config['chunk_size'],
                        max_concurrency=10,
                        multipart_chunksize=self.config['chunk_size'],
                        use_threads=True
                    )
                )
            else:
                self.s3_client.upload_file(file_path, self.config['bucket_name'], s3_key)
            
            self.upload_stats['uploaded_files'] += 1
            self.upload_stats['uploaded_size'] += file_size
            return True
            
        except Exception as e:
            logger.error("Error uploading %s: %s", s3_key, e)
            return False
    
    def upload_files(self, progress_callback=None):
        """Main upload function with progress tracking"""
        if not self.setup_aws_client():
            return False, "Failed to connect to AWS S3"
        
        # Get local files
        local_files = self.get_local_files(self.config['upload_directory'])
        if not local_files:
            return False, "No files found to upload"
        
        # Get existing S3 files
        s3_files = self.get_s3_file_list()
        
        # Filter files that need to be uploaded
        files_to_upload = []
        for file_path, s3_key, size in local_files:
            if s3_key not in s3_files:
                files_to_upload.append((file_path, s3_key, size))
            else:
                self.upload_stats['skipped_files'] += 1
        
        if not files_to_upload:
            return True, "All files are already uploaded"
        
        # Calculate total upload size
        self.upload_stats['total_files'] = len(files_to_upload)
        self.upload_stats['total_size'] = sum(size for _, _, size in files_to_upload)
        
        logger.info("Starting upload of %d files (%s bytes)", len(files_to_upload), f"{self.upload_stats['total_size']:,}")
        
        # Upload files with threading
        successful_uploads = 0
        with ThreadPoolExecutor(max_workers=self.config['max_workers']) as executor:
            future_to_file = {
                executor.submit(self.upload_file, file_path, s3_key, size): (file_path, s3_key, size)
                for file_path, s3_key, size in files_to_upload
            }
            
            for future in as_completed(future_to_file):
                file_path, s3_key, size = future_to_file[future]
                try:
                    if future.result():
                        successful_uploads += 1
                    
                    # Update progress
                    if progress_callback:
                        progress = (self.upload_stats['uploaded_size'] / self.upload_stats['total_size']) * 100
                        progress_callback(progress)
                        
                except Exception as e:
                    logger.error("Error in upload task: %s", e)
        
        return True, f"Upload completed: {successful_uploads}/{len(files_to_upload)} files uploaded"


class NaviUploaderGUI:
    def __init__(self):
        self.uploader = NaviUploader()
        self.root = tk.Tk()
        self.root.title("Navi File Uploader")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Set icon if available
        try:
            if os.path.exists('Navi_logo.jpg'):
                # Convert JPG to ICO for window icon (simplified approach)
                self.root.iconbitmap(default='Navi_logo.jpg')
        except Exception:
            pass  # Icon loading is optional
        
        self.setup_ui()
        self.load_saved_config()
        
        # Auto-start upload if credentials are available
        self.root.after(500, self.check_auto_start)
    
    def setup_ui(self):
        """Create the GUI interface"""
        # Title
        title_label = tk.Label(self.root, text="Navi File Uploader", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)
        
        # Configuration frame - Only AWS credentials needed
        config_frame = tk.LabelFrame(self.root, text="AWS Credentials", padx=10, pady=10)
        config_frame.pack(fill="x", padx=20, pady=10)
        
        # Show current settings (read-only)
        info_text = f"S3 Bucket: {self.uploader.config['bucket_name']}\n"
        info_text += f"AWS Region: {self.uploader.config['aws_region']}\n"
        info_text += f"Upload Directory: {self.uploader.config['upload_directory']}"
        
        info_label = tk.Label(config_frame, text=info_text, font=("Arial", 9), 
                             justify="left", bg="#f0f0f0", relief="sunken", padx=10, pady=5)
        info_label.grid(row=0, columnspan=2, pady=(0, 10), sticky="ew")
        
        # AWS Access Key
        tk.Label(config_frame, text="AWS Access Key ID:").grid(row=1, column=0, sticky="w", pady=2)
        self.access_key_entry = tk.Entry(config_frame, width=50, show="*")
        self.access_key_entry.grid(row=1, column=1, pady=2)
        
        # AWS Secret Key
        tk.Label(config_frame, text="AWS Secret Access Key:").grid(row=2, column=0, sticky="w", pady=2)
        self.secret_key_entry = tk.Entry(config_frame, width=50, show="*")
        self.secret_key_entry.grid(row=2, column=1, pady=2)
        
        # Save config button
        save_button = tk.Button(config_frame, text="Save AWS Credentials", command=self.save_configuration)
        save_button.grid(row=3, columnspan=2, pady=10)
        
        # Progress frame
        progress_frame = tk.LabelFrame(self.root, text="Upload Progress", padx=10, pady=10)
        progress_frame.pack(fill="x", padx=20, pady=10)
        
        self.progress_label = tk.Label(progress_frame, text="Ready to upload")
        self.progress_label.pack(pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100, length=400)
        self.progress_bar.pack(pady=5)
        
        # Control buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        self.upload_button = tk.Button(button_frame, text="Start Upload", command=self.start_upload, 
                                     bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), 
                                     padx=20, pady=10)
        self.upload_button.pack(side="left", padx=10)
        
        test_button = tk.Button(button_frame, text="Test Connection", command=self.test_connection,
                              bg="#2196F3", fg="white", font=("Arial", 12), padx=20, pady=10)
        test_button.pack(side="left", padx=10)
    
    def load_saved_config(self):
        """Load saved AWS credentials into GUI fields"""
        config = self.uploader.config
        self.access_key_entry.insert(0, config.get('aws_access_key_id', ''))
        self.secret_key_entry.insert(0, config.get('aws_secret_access_key', ''))
    
    def save_configuration(self, show_dialog=True):
        """Save AWS credentials to configuration file"""
        # Keep existing config but update only AWS credentials
        config = self.uploader.config.copy()
        config.update({
            'aws_access_key_id': self.access_key_entry.get(),
            'aws_secret_access_key': self.secret_key_entry.get(),
        })
        
        self.uploader.config = config
        self.uploader.save_config(config)
        
        if show_dialog:
            messagebox.showinfo("Success", "AWS credentials saved successfully!")
    
    def test_connection(self):
        """Test AWS S3 connection"""
        self.save_configuration(show_dialog=False)  # Save current config first (silently)
        
        if self.uploader.setup_aws_client():
            messagebox.showinfo("Success", "AWS S3 connection successful!")
        else:
            messagebox.showerror("Error", "Failed to connect to AWS S3. Please check your credentials.")
    
    def update_progress(self, progress):
        """Update progress bar and label"""
        self.progress_var.set(progress)
        self.progress_label.config(text=f"Upload Progress: {progress:.1f}%")
        self.root.update_idletasks()
    
    def start_upload(self, is_auto_start=False):
        """Start the upload process in a separate thread"""
        # Save current config (silently if auto-starting)
        self.save_configuration(show_dialog=not is_auto_start)
        
        # Validate AWS credentials
        if not all([self.uploader.config['aws_access_key_id'],
                   self.uploader.config['aws_secret_access_key']]):
            messagebox.showerror("Error", "Please enter your AWS credentials")
            return
        
        if not os.path.exists(self.uploader.config['upload_directory']):
            messagebox.showerror("Error", f"Upload directory does not exist: {self.uploader.config['upload_directory']}")
            return
        
        # Disable upload button during upload
        self.upload_button.config(state="disabled", text="Uploading...")
        self.progress_var.set(0)
        self.progress_label.config(text="Starting upload...")
        
        # Start upload in separate thread
        upload_thread = threading.Thread(target=self.run_upload)
        upload_thread.daemon = True
        upload_thread.start()
    
    def run_upload(self):
        """Run the actual upload process"""
        try:
            success, message = self.uploader.upload_files(self.update_progress)
            
            # Update UI on main thread
            self.root.after(0, self.upload_complete, success, message)
            
        except Exception as e:
            error_msg = f"Upload error: {str(e)}"
            self.root.after(0, self.upload_complete, False, error_msg)
    
    def upload_complete(self, success, message):
        """Handle upload completion"""
        self.upload_button.config(state="normal", text="Start Upload")
        
        if success:
            self.progress_var.set(100)
            self.progress_label.config(text="Upload completed successfully!")
            messagebox.showinfo("Success", message)
            
            # Auto-close after successful upload (with delay for user to see result)
            self.root.after(3000, self.close_application)
        else:
            self.progress_label.config(text="Upload failed")
            messagebox.showerror("Error", message)
    
    def close_application(self):
        """Clean exit of application"""
        self.root.quit()
        self.root.destroy()
    
    def check_auto_start(self):
        """Check if we can auto-start upload based on existing credentials"""
        if (self.uploader.config.get('aws_access_key_id') and 
            self.uploader.config.get('aws_secret_access_key') and
            os.path.exists(self.uploader.config['upload_directory'])):
            
            # Show auto-start message
            self.progress_label.config(text="Auto-starting upload with saved credentials...")
            self.root.update_idletasks()
            
            # Start upload automatically after a short delay (silent mode)
            self.root.after(1000, lambda: self.start_upload(is_auto_start=True))
        else:
            self.progress_label.config(text="Please enter AWS credentials to begin")
    
    def run(self):
        """Start the GUI application"""
        try:
            self.root.mainloop()
        finally:
            # Ensure clean exit and close terminal
            self.root.quit()
            self.root.destroy()


def main():
    """Main entry point"""
    # Check if running in GUI mode (default) or console mode
    if len(sys.argv) > 1 and sys.argv[1] == '--console':
        # Console mode for debugging
        uploader = NaviUploader()
        if uploader.setup_aws_client():
            success, message = uploader.upload_files()
            print(message)
            return 0 if success else 1
        else:
            print("Failed to setup AWS client")
            return 1
    else:
        # GUI mode
        try:
            app = NaviUploaderGUI()
            app.run()
            return 0
        except Exception as e:
            logger.error("GUI error: %s", e)
            return 1


if __name__ == "__main__":
    sys.exit(main())
