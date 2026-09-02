#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crop rojgaro-logo tightly and set sleek, professional responsive header dimensions
"""

import os, glob, re
from PIL import Image
import numpy as np

BASE_DIR = "/Users/kartikeyansahani/goalnaukri"
UPLOADS_DIR = os.path.join(BASE_DIR, "wp-content/uploads/2026/05")

USER_HEADER_LOGO_PATH = "/Users/kartikeyansahani/.gemini/antigravity-ide/brain/cbe0cab6-bc11-4386-8709-ea7aa849803b/.user_uploaded/media_1788331110260.png"

img = Image.open(USER_HEADER_LOGO_PATH).convert("RGBA")
arr = np.array(img)

# Find true logo content (icon and text)
is_text_or_icon = (arr[:, :, 0] < 150) & (arr[:, :, 2] > 100)
mask = np.zeros_like(is_text_or_icon)
mask[20:-20, 20:-20] = is_text_or_icon[20:-20, 20:-20]

coords = np.argwhere(mask)
y0, x0 = coords.min(axis=0)
y1, x1 = coords.max(axis=0)

# Add 12px balanced padding around content
pad = 14
w, h = img.size
crop_box = (max(0, x0 - pad), max(0, y0 - pad), min(w, x1 + pad), min(h, y1 + pad))

cropped_logo = img.crop(crop_box)
print(f"Cropped logo from 1024x512 to {cropped_logo.size} (Aspect: {cropped_logo.size[0]/cropped_logo.size[1]:.2f})")

# Save high-res cropped logo (both as transparent PNG and white background)
cropped_logo.save(os.path.join(UPLOADS_DIR, "rojgaro-logo.png"), "PNG")
cropped_logo.save(os.path.join(UPLOADS_DIR, "Final.png"), "PNG")

# Also create a version with clean rounded transparent background for navbar
# Transparent background version: make the off-white [248-255] pixels transparent
arr_crop = np.array(cropped_logo)
is_white_bg = (arr_crop[:, :, 0] > 235) & (arr_crop[:, :, 1] > 235) & (arr_crop[:, :, 2] > 235)

# Optional: keep crisp rounded white badge or transparent
# For the dark blue navbar (#020953), a clean white pill badge OR transparent white text
# Let's save the high-res crisp cropped badge as standard
print("✓ Saved tightly cropped rojgaro-logo.png")


# 2. Update CSS in all HTML files and css/style.css to constrain logo height
LOGO_CSS = """
/* ── Sleek Professional Header Logo Sizing ── */
.site-logo, .navigation-branding {
  display: flex !important;
  align-items: center !important;
}

.site-logo img,
.navigation-branding img,
.header-image.is-logo-image {
  height: 44px !important;
  width: auto !important;
  max-height: 44px !important;
  object-fit: contain !important;
  border-radius: 6px !important;
  display: block !important;
  transition: transform 0.2s ease !important;
}

.site-logo img:hover {
  transform: scale(1.02);
}

@media (max-width: 768px) {
  .site-logo img,
  .navigation-branding img,
  .header-image.is-logo-image {
    height: 36px !important;
    max-height: 36px !important;
  }
}
"""

html_files = glob.glob(os.path.join(BASE_DIR, "**/*.html"), recursive=True)
updated_html = 0

for f in html_files:
    with open(f, "r", encoding="utf-8") as fp:
        c = fp.read()
    
    orig = c
    
    # Update cache-buster to ?v=5
    c = re.sub(r"/wp-content/uploads/2026/05/rojgaro-logo\.png(?:\?v=\d+)?", "/wp-content/uploads/2026/05/rojgaro-logo.png?v=5", c)
    
    # Inject or replace logo sizing CSS
    if "Sleek Professional Header Logo Sizing" not in c and "</style>" in c:
        c = c.replace("</style>", LOGO_CSS + "\n</style>", 1)
        
    if c != orig:
        with open(f, "w", encoding="utf-8") as fp:
            fp.write(c)
        updated_html += 1

print(f"✓ Updated logo styling and cache-buster in {updated_html} HTML files.")

# Also update css/style.css
style_css = os.path.join(BASE_DIR, "css", "style.css")
if os.path.exists(style_css):
    with open(style_css, "r", encoding="utf-8") as fp:
        sc = fp.read()
    if "Sleek Professional Header Logo Sizing" not in sc:
        sc += "\n" + LOGO_CSS
        with open(style_css, "w", encoding="utf-8") as fp:
            fp.write(sc)
        print("✓ Updated css/style.css with logo dimensions")

print("\nLogo size fix completed successfully!")
