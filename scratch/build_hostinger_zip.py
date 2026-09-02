#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build complete production ZIP file for Hostinger deployment (public_html)
"""

import os
import zipfile

BASE_DIR = "/Users/kartikeyansahani/goalnaukri"
ZIP_OUTPUT_PATH = os.path.join(BASE_DIR, "rojgaro_hostinger_deploy.zip")

EXCLUDE_DIRS = {".git", "node_modules", "scratch", ".gemini", "__pycache__"}
EXCLUDE_EXTS = {".py", ".log", ".tmp"}
EXCLUDE_FILES = {"rojgaro_hostinger_deploy.zip", "package-lock.json"}

total_files = 0
total_size = 0

with zipfile.ZipFile(ZIP_OUTPUT_PATH, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(BASE_DIR):
        # Modify dirs in-place to skip excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            if file in EXCLUDE_FILES or any(file.endswith(ext) for ext in EXCLUDE_EXTS):
                continue
                
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, BASE_DIR)
            
            zipf.write(file_path, arcname)
            total_files += 1
            total_size += os.path.getsize(file_path)

zip_size_mb = os.path.getsize(ZIP_OUTPUT_PATH) / (1024 * 1024)
print(f"✓ Created Hostinger Production ZIP: {ZIP_OUTPUT_PATH}")
print(f"✓ Total files packaged: {total_files}")
print(f"✓ Uncompressed size: {total_size / (1024 * 1024):.2f} MB")
print(f"✓ ZIP archive size: {zip_size_mb:.2f} MB")
