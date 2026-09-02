#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build accurate pagination for Page 1, Page 2, Page 3 and Category pages
"""

import os
import re
import urllib.request
import urllib.parse

BASE_DIR = "/Users/kartikeyansahani/goalnaukri"

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

# Read template from index.html
with open(os.path.join(BASE_DIR, "index.html"), "r", encoding="utf-8") as fp:
    index_html = fp.read()

# Separate template before and after main
head_template = index_html.split('<main id="main" class="site-main">')[0] + '<main id="main" class="site-main">\n'
tail_template = '\n      </main>' + index_html.split('</main>')[1]

def clean_main_content(raw_main_html, page_num, total_pages=3, is_category=False):
    content = raw_main_html
    
    # Download any remote images in cards
    imgs = re.findall(r'<img[^>]+src=["\'](https://goalnaukri\.com/wp-content/uploads/[^"\']+)["\']', content)
    for in_img in imgs:
        local_in = download_image(in_img)
        content = content.replace(in_img, local_in)
        
    # Replace absolute URLs to relative URLs
    content = content.replace("https://goalnaukri.com/wp-content/uploads/", "/wp-content/uploads/")
    content = content.replace("https://goalnaukri.com/", "/")
    content = content.replace("https://rojgaro.com/wp-content/uploads/", "/wp-content/uploads/")
    content = content.replace("https://rojgaro.com/", "/")
    
    # Replace branding
    content = content.replace("Goal Naukri", "Rojgaro").replace("GoalNaukri", "Rojgaro")
    
    # Replace or build custom pagination bar
    prefix = "/category/career-guide/" if is_category else "/"
    p_prefix = "/category/career-guide/page/" if is_category else "/page/"
    
    nav_links = []
    if page_num > 1:
        prev_url = prefix if page_num == 2 else f"{p_prefix}{page_num - 1}/"
        nav_links.append(f'<a class="prev page-numbers" href="{prev_url}">« Previous</a>')
        
    for p in range(1, total_pages + 1):
        p_url = prefix if p == 1 else f"{p_prefix}{p}/"
        if p == page_num:
            nav_links.append(f'<span aria-current="page" class="page-numbers current">{p}</span>')
        else:
            nav_links.append(f'<a class="page-numbers" href="{p_url}">{p}</a>')
            
    if page_num < total_pages:
        next_url = f"{p_prefix}{page_num + 1}/"
        nav_links.append(f'<a class="next page-numbers" href="{next_url}">Next »</a>')
        
    custom_pagination_html = f"""
<nav class="paging-navigation" aria-label="Posts">
  <div class="pagination loop-pagination">
    {' '.join(nav_links)}
  </div>
</nav>
"""
    # Remove old paging navigation if present and append custom
    if '<nav class="paging-navigation"' in content:
        content = re.sub(r'<nav class="paging-navigation".*?</nav>', custom_pagination_html, content, flags=re.DOTALL)
    else:
        content = content + "\n" + custom_pagination_html
        
    return content

# 1. Fetch Page 2 and Page 3 from goalnaukri.com
for page_num in [2, 3]:
    url = f"https://goalnaukri.com/page/{page_num}/"
    print(f"Fetching {url}...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    raw_page_html = urllib.request.urlopen(req, timeout=15).read().decode("utf-8")
    
    main_match = re.search(r'<main class="site-main"[^>]*>(.*?)</main>', raw_page_html, re.DOTALL)
    if not main_match:
        print(f"Failed to find main for page {page_num}")
        continue
        
    cleaned_main = clean_main_content(main_match.group(1), page_num, 3, is_category=False)
    
    # Prepare custom head for page 2/3
    cur_head = head_template
    cur_head = re.sub(r'<title>.*?</title>', f'<title>Page {page_num} of 3 - Rojgaro</title>', cur_head)
    
    page_html = cur_head + cleaned_main + tail_template
    
    target_dir = os.path.join(BASE_DIR, "page", str(page_num))
    os.makedirs(target_dir, exist_ok=True)
    target_file = os.path.join(target_dir, "index.html")
    with open(target_file, "w", encoding="utf-8") as fp:
        fp.write(page_html)
    print(f"✓ Saved: page/{page_num}/index.html ({len(page_html)} bytes)")

# 2. Update Page 1 index.html pagination
main_p1_match = re.search(r'<main id="main" class="site-main"[^>]*>(.*?)</main>', index_html, re.DOTALL)
if main_p1_match:
    cleaned_main_p1 = clean_main_content(main_p1_match.group(1), 1, 3, is_category=False)
    updated_index_html = head_template + cleaned_main_p1 + tail_template
    with open(os.path.join(BASE_DIR, "index.html"), "w", encoding="utf-8") as fp:
        fp.write(updated_index_html)
    print("✓ Updated: index.html pagination")

# 3. Build Category Career Guide Pages (Page 1, 2, 3)
for page_num in [1, 2, 3]:
    remote_url = f"https://goalnaukri.com/category/career-guide/page/{page_num}/" if page_num > 1 else "https://goalnaukri.com/category/career-guide/"
    print(f"Fetching category {remote_url}...")
    req = urllib.request.Request(remote_url, headers={"User-Agent": "Mozilla/5.0"})
    raw_cat_html = urllib.request.urlopen(req, timeout=15).read().decode("utf-8")
    
    main_match = re.search(r'<main class="site-main"[^>]*>(.*?)</main>', raw_cat_html, re.DOTALL)
    if not main_match:
        print(f"Failed to find category main for page {page_num}")
        continue
        
    cleaned_cat_main = clean_main_content(main_match.group(1), page_num, 3, is_category=True)
    
    cur_head = head_template
    cat_title = "Career Guide - Rojgaro" if page_num == 1 else f"Career Guide - Page {page_num} of 3 - Rojgaro"
    cur_head = re.sub(r'<title>.*?</title>', f'<title>{cat_title}</title>', cur_head)
    
    # Add page header for category if present
    cat_header = '<header class="page-header"><h1 class="page-title">Category: Career Guide</h1></header>\n'
    cat_page_html = cur_head + cat_header + cleaned_cat_main + tail_template
    
    if page_num == 1:
        with open(os.path.join(BASE_DIR, "category", "career-guide.html"), "w", encoding="utf-8") as fp:
            fp.write(cat_page_html)
        target_dir = os.path.join(BASE_DIR, "category", "career-guide")
        os.makedirs(target_dir, exist_ok=True)
        with open(os.path.join(target_dir, "index.html"), "w", encoding="utf-8") as fp:
            fp.write(cat_page_html)
        print("✓ Saved: category/career-guide.html & category/career-guide/index.html")
    else:
        target_dir = os.path.join(BASE_DIR, "category", "career-guide", "page", str(page_num))
        os.makedirs(target_dir, exist_ok=True)
        with open(os.path.join(target_dir, "index.html"), "w", encoding="utf-8") as fp:
            fp.write(cat_page_html)
        print(f"✓ Saved: category/career-guide/page/{page_num}/index.html")

print("\nPagination build completed successfully!")
