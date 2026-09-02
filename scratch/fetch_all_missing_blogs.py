#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fetch and build all 14 missing blog posts from goalnaukri.com
"""

import os
import re
import urllib.request
import urllib.parse

BASE_DIR = "/Users/kartikeyansahani/goalnaukri"

MISSING_SLUGS = [
    "iti-trade-best-for-railway-jobs",
    "job-available-after-doing-bca",
    "how-to-become-a-government-teacher-in-bihar",
    "become-a-bihar-police-officer",
    "what-degree-is-needed-to-become-a-ceo",
    "best-course-in-medical-field",
    "what-jobs-do-upsc-pass-candidates-get",
    "become-ips",
    "become-computer-engineer",
    "how-to-become-a-bank-manager",
    "ssc-chsl-preparation",
    "ssc-cgl-preparation-strategy",
    "worlds-smartest-ai",
    "iti-career-options"
]

# Read reference template from how-to-prepare-for-the-air-force-after-class-12.html
with open(os.path.join(BASE_DIR, "how-to-prepare-for-the-air-force-after-class-12.html"), "r", encoding="utf-8") as fp:
    sample_html = fp.read()

# Separate template before and after entry-content
head_template = sample_html.split("<div class=\"entry-content\">")[0]
tail_template = sample_html.split("</div>\n        <div class=\"irt-author-box\"")[1]

def download_image(img_url):
    """Download image to local wp-content/uploads if from goalnaukri/rojgaro"""
    if not img_url or "wp-content/uploads" not in img_url:
        return img_url
    
    path_part = img_url.split("wp-content/uploads/")[1].split("?")[0]
    parts = path_part.split("/")
    encoded_parts = [urllib.parse.quote(p) for p in parts]
    encoded_path = "/".join(encoded_parts)
    source_url = f"https://goalnaukri.com/wp-content/uploads/{encoded_path}"
    
    local_target = os.path.join(BASE_DIR, "wp-content", "uploads", path_part)
    os.makedirs(os.path.dirname(local_target), exist_ok=True)
    
    if not os.path.exists(local_target) or os.path.getsize(local_target) == 0:
        try:
            req = urllib.request.Request(
                source_url,
                headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
            )
            with urllib.request.urlopen(req, timeout=15) as resp, open(local_target, "wb") as out:
                out.write(resp.read())
            print(f"  ✓ Downloaded image: {path_part}")
        except Exception as e:
            print(f"  ✗ Failed downloading image {source_url}: {e}")
            
    return f"/wp-content/uploads/{path_part}"

for idx, slug in enumerate(MISSING_SLUGS, 1):
    url = f"https://goalnaukri.com/{slug}/"
    print(f"\n[{idx}/14] Fetching {url}...")
    
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"})
        raw_html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8")
    except Exception as e:
        print(f"Error fetching {slug}: {e}")
        continue
        
    # Extract Title
    title_m = re.search(r"<h1[^>]*>(.*?)</h1>", raw_html)
    title = title_m.group(1).strip() if title_m else slug.replace("-", " ").title()
    title = re.sub(r"\s+", " ", title)
    
    # Extract Description
    desc_m = re.search(r"<meta name=\"description\" content=\"([^\"]+)\"", raw_html)
    desc = desc_m.group(1).strip() if desc_m else title
    
    # Extract Date
    date_m = re.search(r"<time class=\"entry-date published\" datetime=\"([^\"]+)\">([^<]+)</time>", raw_html)
    if date_m:
        datetime_val = date_m.group(1)
        date_display = date_m.group(2)
    else:
        date_m2 = re.search(r"<time[^>]+datetime=\"([^\"]+)\"[^>]*>([^<]+)</time>", raw_html)
        if date_m2:
            datetime_val = date_m2.group(1)
            date_display = date_m2.group(2)
        else:
            datetime_val = "2026-05-15T12:00:00+05:30"
            date_display = "May 15, 2026"
            
    # Extract Featured Image
    img_m = re.search(r"<meta property=\"og:image\" content=\"([^\"]+)\"", raw_html)
    featured_img_url = img_m.group(1) if img_m else ""
    if not featured_img_url:
        img_m2 = re.search(r"<div class=\"post-image\"[^>]*>.*?<img[^>]+src=\"([^\"]+)\"", raw_html, re.DOTALL)
        featured_img_url = img_m2.group(1) if img_m2 else ""
        
    local_featured_img = download_image(featured_img_url)
    if not local_featured_img:
        local_featured_img = "/wp-content/uploads/2026/05/Final.png"
        
    # Extract Content
    content_match = re.search(r"<div class=\"entry-content\"[^>]*>(.*?)(?:</div>\s*</div>\s*<div class=\"irt-author-box\"|</div>\s*</div>\s*</article>|<footer class=\"entry-meta\"|<div class=\"comments-area\")", raw_html, re.DOTALL)
    if content_match:
        content = content_match.group(1).strip()
    else:
        content_match2 = re.search(r"<div class=\"entry-content\"[^>]*>(.*)", raw_html, re.DOTALL)
        if content_match2:
            # cut before author box or footer
            c = content_match2.group(1)
            for stop in ["<div class=\"irt-author-box\"", "<div class=\"comments-area\"", "<div class=\"site-footer\"", "</article>"]:
                if stop in c:
                    c = c.split(stop)[0]
            content = c.strip()
        else:
            content = "<p>" + desc + "</p>"
            
    # Download any inline images within content
    inline_imgs = re.findall(r"<img[^>]+src=[\"\x27](https://goalnaukri\.com/wp-content/uploads/[^\"\x27]+)[\"\x27]", content)
    for in_img in inline_imgs:
        local_in = download_image(in_img)
        content = content.replace(in_img, local_in)
        
    # Clean content branding
    content = content.replace("Goal Naukri", "Rojgaro").replace("GoalNaukri", "Rojgaro").replace("goalnaukri.com", "rojgaro.com").replace("goalnaukri", "rojgaro")
    content = content.replace("Akshay Sahni", "Kartikeyan Sahani").replace("अक्षय सहनी", "कार्तिकेयन साहनी").replace("अक्षय साहनी", "कार्तिकेयन साहनी")
    
    # Build Custom Head
    # Update title and description in head
    page_head = head_template
    page_head = re.sub(r"<title>.*?</title>", f"<title>{title} - Rojgaro</title>", page_head)
    page_head = re.sub(r"<meta name=\"description\" content=\".*?\">", f'<meta name="description" content="{desc}">', page_head)
    page_head = re.sub(r"<h1 class=\"entry-title\"[^>]*>.*?</h1>", f'<h1 class="entry-title" itemprop="headline">{title}</h1>', page_head)
    page_head = re.sub(r"<time class=\"entry-date published\" datetime=\".*?\">.*?</time>", f'<time class="entry-date published" datetime="{datetime_val}" itemprop="datePublished">{date_display}</time>', page_head)
    
    # Update post image in head
    page_head = re.sub(r'<div class="post-image">.*?</div>', f'<div class="post-image">\n          <img width="1280" height="720" src="{local_featured_img}" class="attachment-full size-full" alt="{title}" itemprop="image">\n        </div>', page_head, flags=re.DOTALL)
    
    # Combine full page
    full_html = page_head + '<div class="entry-content">\n' + content + '\n          </div>\n        </div>\n        <div class="irt-author-box"' + tail_template
    
    # Write slug.html
    root_file = os.path.join(BASE_DIR, f"{slug}.html")
    with open(root_file, "w", encoding="utf-8") as out_fp:
        out_fp.write(full_html)
        
    # Write slug/index.html
    sub_dir = os.path.join(BASE_DIR, slug)
    os.makedirs(sub_dir, exist_ok=True)
    sub_file = os.path.join(sub_dir, "index.html")
    with open(sub_file, "w", encoding="utf-8") as out_fp:
        out_fp.write(full_html)
        
    print(f"  ✓ Saved: {slug}.html & {slug}/index.html ({len(full_html)} bytes)")

print("\nAll 14 missing blog posts processed successfully!")
