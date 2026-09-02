#!/usr/bin/env python3
import glob, re

social_links = {}

patterns = [
    (r"https?://(?:www\.)?whatsapp\.com/[^\s\"\'\<\>]+", "WhatsApp"),
    (r"https?://(?:www\.)?api\.whatsapp\.com/[^\s\"\'\<\>]+", "WhatsApp API"),
    (r"https?://(?:www\.)?t\.me/[^\s\"\'\<\>]+", "Telegram"),
    (r"https?://(?:www\.)?telegram\.me/[^\s\"\'\<\>]+", "Telegram"),
    (r"https?://(?:www\.)?youtube\.com/[^\s\"\'\<\>]+", "YouTube"),
    (r"https?://(?:www\.)?youtu\.be/[^\s\"\'\<\>]+", "YouTube"),
    (r"https?://(?:www\.)?twitter\.com/[^\s\"\'\<\>]+", "Twitter/X"),
    (r"https?://(?:www\.)?x\.com/[^\s\"\'\<\>]+", "Twitter/X"),
    (r"https?://(?:www\.)?facebook\.com/[^\s\"\'\<\>]+", "Facebook"),
    (r"https?://(?:www\.)?instagram\.com/[^\s\"\'\<\>]+", "Instagram"),
    (r"https?://(?:www\.)?linkedin\.com/[^\s\"\'\<\>]+", "LinkedIn"),
    (r"https?://(?:www\.)?threads\.net/[^\s\"\'\<\>]+", "Threads"),
    (r"https?://(?:www\.)?pinterest\.com/[^\s\"\'\<\>]+", "Pinterest")
]

for f in glob.glob("**/*.html", recursive=True):
    with open(f, "r", encoding="utf-8") as fp:
        c = fp.read()
    
    for pat, platform in patterns:
        matches = re.findall(pat, c)
        for m in matches:
            clean_url = m.rstrip('",;>')
            if clean_url not in social_links:
                social_links[clean_url] = {"platform": platform, "files_count": 0, "sample_files": []}
            social_links[clean_url]["files_count"] += 1
            if len(social_links[clean_url]["sample_files"]) < 3:
                social_links[clean_url]["sample_files"].append(f)

print(f"Total Unique Social Media Links: {len(social_links)}\n")
for url, info in sorted(social_links.items(), key=lambda x: x[1]["platform"]):
    print(f"📌 Platform: {info['platform']}")
    print(f"   URL: {url}")
    print(f"   Usage Count: {info['files_count']} files")
    print(f"   Example files: {info['sample_files']}")
    print()
