#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix YouTube video embeds and image responsiveness across all HTML files and style.css
"""

import glob, os, re

BASE_DIR = "/Users/kartikeyansahani/goalnaukri"

RESPONSIVE_VIDEO_CSS = """
/* ── Responsive Video Embeds & Image Fix ── */
.wp-block-embed,
.wp-block-embed-youtube,
.wp-embed-aspect-16-9,
.wp-has-aspect-ratio,
figure.wp-block-embed {
  position: relative !important;
  width: 100% !important;
  max-width: 100% !important;
  margin: 28px 0 !important;
  padding: 0 !important;
  overflow: hidden !important;
}

.wp-block-embed__wrapper {
  position: relative !important;
  width: 100% !important;
  padding-bottom: 56.25% !important; /* 16:9 aspect ratio */
  height: 0 !important;
  overflow: hidden !important;
  border-radius: 8px !important;
  background: #000 !important;
}

.wp-block-embed__wrapper iframe,
.wp-block-embed iframe,
.entry-content iframe,
iframe {
  position: absolute !important;
  top: 0 !important;
  left: 0 !important;
  width: 100% !important;
  height: 100% !important;
  max-width: 100% !important;
  border: 0 !important;
  border-radius: 8px !important;
}

/* Ensure images and figures never overflow viewport */
img, figure, .post-image, .gb-block-image {
  max-width: 100% !important;
  height: auto !important;
  box-sizing: border-box !important;
}

figure {
  margin: 0 0 20px 0 !important;
}

@media (max-width: 768px) {
  .wp-block-embed,
  .wp-block-embed-youtube {
    margin: 20px 0 !important;
  }
  .entry-content {
    overflow-x: hidden !important;
  }
}
"""

html_files = glob.glob(os.path.join(BASE_DIR, "**/*.html"), recursive=True)
updated_count = 0

for f in html_files:
    with open(f, "r", encoding="utf-8") as fp:
        c = fp.read()
        
    orig = c
    
    # Inject responsive CSS before </style>
    if "</style>" in c and "Responsive Video Embeds" not in c:
        c = c.replace("</style>", RESPONSIVE_VIDEO_CSS + "\n</style>", 1)
        
    if c != orig:
        with open(f, "w", encoding="utf-8") as fp:
            fp.write(c)
        updated_count += 1

print(f"✓ Injected responsive video CSS in {updated_count} HTML files.")

# Also add to style.css
style_css_path = os.path.join(BASE_DIR, "css", "style.css")
if os.path.exists(style_css_path):
    with open(style_css_path, "r", encoding="utf-8") as fp:
        sc = fp.read()
    if "Responsive Video Embeds" not in sc:
        sc += "\n" + RESPONSIVE_VIDEO_CSS
        with open(style_css_path, "w", encoding="utf-8") as fp:
            fp.write(sc)
        print("✓ Injected responsive video CSS in css/style.css")

print("\nVideo and image mobile responsiveness fix completed successfully!")
