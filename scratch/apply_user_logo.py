#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Apply user's official uploaded logo and icon across the entire website
"""

import os, glob, re
from PIL import Image

BASE_DIR = "/Users/kartikeyansahani/goalnaukri"
UPLOADS_DIR = os.path.join(BASE_DIR, "wp-content/uploads/2026/05")
os.makedirs(UPLOADS_DIR, exist_ok=True)

USER_ICON_PATH = "/Users/kartikeyansahani/.gemini/antigravity-ide/brain/cbe0cab6-bc11-4386-8709-ea7aa849803b/.user_uploaded/media_1788331110236.png"
USER_HEADER_LOGO_PATH = "/Users/kartikeyansahani/.gemini/antigravity-ide/brain/cbe0cab6-bc11-4386-8709-ea7aa849803b/.user_uploaded/media_1788331110260.png"

# 1. Process Header Logo
im_logo = Image.open(USER_HEADER_LOGO_PATH)

# Crop white/transparent borders if any
bbox = im_logo.getbbox()
if bbox:
    # Add a slight padding
    w, h = im_logo.size
    pad = 10
    crop_box = (max(0, bbox[0]-pad), max(0, bbox[1]-pad), min(w, bbox[2]+pad), min(h, bbox[3]+pad))
    im_logo_cropped = im_logo.crop(crop_box)
else:
    im_logo_cropped = im_logo

im_logo_cropped.save(os.path.join(UPLOADS_DIR, "rojgaro-logo.png"), "PNG")
im_logo_cropped.save(os.path.join(UPLOADS_DIR, "Final.png"), "PNG")
print("✓ Saved official header logo to rojgaro-logo.png and Final.png")


# 2. Process Icon & Favicon
im_icon = Image.open(USER_ICON_PATH)

im_icon.save(os.path.join(UPLOADS_DIR, "rojgaro-icon.png"), "PNG")
im_icon.convert("RGB").save(os.path.join(UPLOADS_DIR, "rojgaro-icon.jpg"), quality=95)

# Multi-resolution favicon.ico
ico_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
im_icon.save(os.path.join(BASE_DIR, "favicon.ico"), format="ICO", sizes=ico_sizes)
print("✓ Created multi-resolution favicon.ico from user icon")

# Icon sizes
sizes = {
    "rojgaro-icon-512x512.png": 512,
    "rojgaro-icon-270x270.png": 270,
    "rojgaro-icon-192x192.png": 192,
    "rojgaro-icon-180x180.png": 180,
    "rojgaro-icon-32x32.png": 32,
    "cropped-GN-Fevicon-Icon-32x32.jpg": 32,
    "cropped-GN-Fevicon-Icon-180x180.jpg": 180,
    "cropped-GN-Fevicon-Icon-192x192.jpg": 192,
    "cropped-GN-Fevicon-Icon-270x270.jpg": 270,
    "rojgaro-favicon-Icon-32x32.jpg": 32,
    "cropped-rojgaro-favicon-Icon-32x32.jpg": 32,
}

for name, s in sizes.items():
    resized = im_icon.resize((s, s), Image.Resampling.LANCZOS)
    if name.endswith(".jpg"):
        resized.convert("RGB").save(os.path.join(UPLOADS_DIR, name), quality=95)
    else:
        resized.save(os.path.join(UPLOADS_DIR, name))
    print(f"✓ Generated {name} ({s}x{s})")


# 3. Update all HTML files with cache buster ?v=4
html_files = glob.glob(os.path.join(BASE_DIR, "**/*.html"), recursive=True)
updated_count = 0

for f in html_files:
    with open(f, "r", encoding="utf-8") as fp:
        c = fp.read()
    
    orig = c
    c = re.sub(r"/wp-content/uploads/2026/05/rojgaro-logo\.png(?:\?v=\d+)?", "/wp-content/uploads/2026/05/rojgaro-logo.png?v=4", c)
    c = re.sub(r"/wp-content/uploads/2026/05/rojgaro-icon-32x32\.png(?:\?v=\d+)?", "/wp-content/uploads/2026/05/rojgaro-icon-32x32.png?v=4", c)
    c = re.sub(r"/wp-content/uploads/2026/05/rojgaro-icon-192x192\.png(?:\?v=\d+)?", "/wp-content/uploads/2026/05/rojgaro-icon-192x192.png?v=4", c)
    c = re.sub(r"/wp-content/uploads/2026/05/rojgaro-icon-180x180\.png(?:\?v=\d+)?", "/wp-content/uploads/2026/05/rojgaro-icon-180x180.png?v=4", c)
    c = re.sub(r"/favicon\.ico(?:\?v=\d+)?", "/favicon.ico?v=4", c)
    
    if c != orig:
        with open(f, "w", encoding="utf-8") as fp:
            fp.write(c)
        updated_count += 1

print(f"\n✓ Updated cache-busted logo and icon tags in {updated_count} HTML files.")
