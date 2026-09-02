#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clean duplicate pagination bars and keep only 1 exact single GenerateBlocks pagination bar
"""

import os
import re

BASE_DIR = "/Users/kartikeyansahani/goalnaukri"

files = [
    "index.html",
    "page/2/index.html",
    "page/3/index.html",
    "category/career-guide.html",
    "category/career-guide/index.html",
    "category/career-guide/page/2/index.html",
    "category/career-guide/page/3/index.html"
]

prev_svg = """<svg aria-hidden="true" role="img" height="1em" width="1em" viewbox="0 0 256 512" xmlns="http://www.w3.org/2000/svg"><path fill="currentColor" d="M31.7 239l136-136c9.4-9.4 24.6-9.4 33.9 0l22.6 22.6c9.4 9.4 9.4 24.6 0 33.9L127.9 256l96.4 96.4c9.4 9.4 9.4 24.6 0 33.9L201.7 409c-9.4 9.4-24.6 9.4-33.9 0l-136-136c-9.5-9.4-9.5-24.6-.1-34z"></path></svg>"""
next_svg = """<svg aria-hidden="true" role="img" height="1em" width="1em" viewbox="0 0 256 512" xmlns="http://www.w3.org/2000/svg"><path fill="currentColor" d="M224.3 273l-136 136c-9.4 9.4-24.6 9.4-33.9 0l-22.6-22.6c-9.4-9.4-9.4-24.6 0-33.9l96.4-96.4-96.4-96.4c-9.4-9.4-9.4-24.6 0-33.9L54.3 103c9.4-9.4 24.6-9.4 33.9 0l136 136c9.5 9.4 9.5 24.6.1 34z"></path></svg>"""

def get_gb_pagination(page_num, is_category=False):
    base_url = "/category/career-guide/" if is_category else "/"
    p2_url = "/category/career-guide/page/2/" if is_category else "/page/2/"
    p3_url = "/category/career-guide/page/3/" if is_category else "/page/3/"
    
    if page_num == 1:
        return f"""<div class="gb-container gb-container-4dc632a1 gb-query-loop-pagination">
<span class="gb-button gb-button-8a92b969 gb-button-text page-numbers gb-block-is-current" aria-current="page">1</span><a class="gb-button gb-button-8a92b969 gb-button-text page-numbers" href="{p2_url}">2</a><a class="gb-button gb-button-8a92b969 gb-button-text page-numbers" href="{p3_url}">3</a>
<a class="gb-button gb-button-0da14d3f" href="{p2_url}"><span class="gb-button-text">Next</span><span class="gb-icon">{next_svg}</span></a>
</div>"""
    elif page_num == 2:
        return f"""<div class="gb-container gb-container-4dc632a1 gb-query-loop-pagination">
<a class="gb-button gb-button-f2c46de0" href="{base_url}"><span class="gb-icon">{prev_svg}</span><span class="gb-button-text">Previous</span></a><a class="gb-button gb-button-8a92b969 gb-button-text page-numbers" href="{base_url}">1</a><span class="gb-button gb-button-8a92b969 gb-button-text page-numbers gb-block-is-current" aria-current="page">2</span><a class="gb-button gb-button-8a92b969 gb-button-text page-numbers" href="{p3_url}">3</a>
<a class="gb-button gb-button-0da14d3f" href="{p3_url}"><span class="gb-button-text">Next</span><span class="gb-icon">{next_svg}</span></a>
</div>"""
    else:
        return f"""<div class="gb-container gb-container-4dc632a1 gb-query-loop-pagination">
<a class="gb-button gb-button-f2c46de0" href="{p2_url}"><span class="gb-icon">{prev_svg}</span><span class="gb-button-text">Previous</span></a><a class="gb-button gb-button-8a92b969 gb-button-text page-numbers" href="{base_url}">1</a><a class="gb-button gb-button-8a92b969 gb-button-text page-numbers" href="{p2_url}">2</a><span class="gb-button gb-button-8a92b969 gb-button-text page-numbers gb-block-is-current" aria-current="page">3</span>
</div>"""

for fpath in files:
    full_path = os.path.join(BASE_DIR, fpath)
    if not os.path.exists(full_path):
        continue
    with open(full_path, "r", encoding="utf-8") as fp:
        c = fp.read()
        
    is_cat = "career-guide" in fpath
    if "page/3" in fpath:
        pnum = 3
    elif "page/2" in fpath:
        pnum = 2
    else:
        pnum = 1
        
    # 1. Remove all instances of <nav class="paging-navigation"...>...</nav>
    c = re.sub(r'\s*<nav class="paging-navigation"[^>]*>.*?</nav>', '', c, flags=re.DOTALL)
    
    # 2. Replace existing gb-query-loop-pagination with exactly 1 clean instance
    new_pag = get_gb_pagination(pnum, is_cat)
    if '<div class="gb-container gb-container-4dc632a1 gb-query-loop-pagination">' in c:
        c = re.sub(r'<div class="gb-container gb-container-4dc632a1 gb-query-loop-pagination">.*?</div>', new_pag, c, flags=re.DOTALL)
    else:
        c = c.replace("</main>", new_pag + "\n</main>", 1)
        
    with open(full_path, "w", encoding="utf-8") as fp:
        fp.write(c)
        
    print(f"✓ Fixed pagination in: {fpath}")

print("\nAll duplicate pagination removed successfully!")
