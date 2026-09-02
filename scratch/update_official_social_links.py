#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Replace all social media links across the entire website with user's official links
"""

import glob, os, re

BASE_DIR = "/Users/kartikeyansahani/goalnaukri"

OLD_WHATSAPP_PATTERNS = [
    r"https?://(?:www\.)?whatsapp\.com/channel/[^\s\"\'\<\>]+",
    r"https?://chat\.whatsapp\.com/(?!Lnb4fxnJTQmJByUOzhxvnT)[^\s\"\'\<\>]+"
]
NEW_WHATSAPP_URL = "https://chat.whatsapp.com/Lnb4fxnJTQmJByUOzhxvnT"

OLD_TELEGRAM_PATTERNS = [
    r"https?://t\.me/\+EV1cAhnn_6gxZTM1[^\s\"\'\<\>]*",
    r"https?://t\.me/(?!rojgaro\b)[^\s\"\'\<\>]+"
]
NEW_TELEGRAM_URL = "https://t.me/rojgaro"

NEW_X_URL = "https://x.com/rojgaro_"
NEW_INSTA_URL = "https://www.instagram.com/rojgaro"

NEW_SAMEAS_JSON = """"sameAs": [
        "https://chat.whatsapp.com/Lnb4fxnJTQmJByUOzhxvnT",
        "https://t.me/rojgaro",
        "https://x.com/rojgaro_",
        "https://www.instagram.com/rojgaro"
      ]"""

files = glob.glob(os.path.join(BASE_DIR, "**/*"), recursive=True)
updated_count = 0

for f in files:
    if os.path.isdir(f) or ".git" in f or "node_modules" in f:
        continue
    if not (f.endswith(".html") or f.endswith(".json") or f.endswith(".md") or f.endswith(".js") or f.endswith(".py")):
        continue
        
    with open(f, "r", encoding="utf-8") as fp:
        c = fp.read()
        
    orig = c
    
    # 1. Replace WhatsApp link
    c = c.replace("https://chat.whatsapp.com/Lnb4fxnJTQmJByUOzhxvnT", NEW_WHATSAPP_URL)
    c = re.sub(r"https://(?:www\.)?whatsapp\.com/channel/[A-Za-z0-9_-]+", NEW_WHATSAPP_URL, c)
    
    # 2. Replace Telegram link
    c = c.replace("https://t.me/rojgaro", NEW_TELEGRAM_URL)
    
    # 3. Replace Twitter / X link
    c = c.replace("https://x.com/rojgaro\"", f"{NEW_X_URL}\"")
    c = c.replace("https://x.com/rojgaro_",", f"{NEW_X_URL}\",")
    
    # 4. Replace Schema sameAs block
    c = re.sub(r'"sameAs":\s*\[[^\]]+\]', NEW_SAMEAS_JSON, c)
    
    if c != orig:
        with open(f, "w", encoding="utf-8") as fp:
            fp.write(c)
        updated_count += 1
        if f.endswith(".html"):
            print(f"✓ Updated links in: {os.path.relpath(f, BASE_DIR)}")

print(f"\nTotal files updated with official social media links: {updated_count}")
