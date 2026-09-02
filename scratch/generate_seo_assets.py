#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate robots.txt, full XML sitemaps, and fix missing H1 tags for 100% SEO audit pass
"""

import os
import glob
import re
from datetime import datetime

BASE_DIR = "/Users/kartikeyansahani/goalnaukri"
DOMAIN = "https://rojgaro.com"
TODAY = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")

# 1. Create robots.txt
robots_txt_content = f"""User-agent: *
Allow: /
Disallow: /scratch/
Disallow: /.git/

Sitemap: {DOMAIN}/sitemap.xml
Sitemap: {DOMAIN}/sitemap_index.xml
"""

with open(os.path.join(BASE_DIR, "robots.txt"), "w", encoding="utf-8") as fp:
    fp.write(robots_txt_content)
print("✓ Created robots.txt")


# 2. Collect all URLs
# Posts (24 blog posts)
blog_slugs = [
    "how-to-prepare-for-the-air-force-after-class-12",
    "ntpc-sail-recruitment-2026",
    "what-kind-of-jobs-can-i-get-after-completing-an-mba",
    "what-kind-of-job-can-i-get-after-doing-b-sc",
    "benefits-of-vocational-courses",
    "how-is-the-chief-justice-of-india-selected",
    "what-kind-of-jobs-do-you-get-after-doing-polytechnic",
    "what-it-takes-to-become-an-electrical-engineer",
    "what-does-it-take-to-get-a-job-at-google",
    "what-it-takes-to-become-a-chemical-engineer",
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

# Static pages
static_pages = [
    "about-us",
    "contact-us",
    "privacy-policy",
    "disclaimer",
    "term-and-conditions"
]

# Category pages
categories = [
    "category/career-guide"
]

# Generate post-sitemap.xml
post_sitemap_urls = []
for slug in blog_slugs:
    post_sitemap_urls.append(f"""\t<url>
\t\t<loc>{DOMAIN}/{slug}/</loc>
\t\t<lastmod>{TODAY}</lastmod>
\t\t<changefreq>weekly</changefreq>
\t\t<priority>0.8</priority>
\t</url>""")

post_sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(post_sitemap_urls)}
</urlset>"""

with open(os.path.join(BASE_DIR, "post-sitemap.xml"), "w", encoding="utf-8") as fp:
    fp.write(post_sitemap)
print("✓ Created post-sitemap.xml")

# Generate page-sitemap.xml
page_sitemap_urls = [f"""\t<url>
\t\t<loc>{DOMAIN}/</loc>
\t\t<lastmod>{TODAY}</lastmod>
\t\t<changefreq>daily</changefreq>
\t\t<priority>1.0</priority>
\t</url>"""]

for slug in static_pages:
    page_sitemap_urls.append(f"""\t<url>
\t\t<loc>{DOMAIN}/{slug}/</loc>
\t\t<lastmod>{TODAY}</lastmod>
\t\t<changefreq>monthly</changefreq>
\t\t<priority>0.6</priority>
\t</url>""")

page_sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(page_sitemap_urls)}
</urlset>"""

with open(os.path.join(BASE_DIR, "page-sitemap.xml"), "w", encoding="utf-8") as fp:
    fp.write(page_sitemap)
print("✓ Created page-sitemap.xml")

# Generate category-sitemap.xml
cat_sitemap_urls = []
for slug in categories:
    cat_sitemap_urls.append(f"""\t<url>
\t\t<loc>{DOMAIN}/{slug}/</loc>
\t\t<lastmod>{TODAY}</lastmod>
\t\t<changefreq>weekly</changefreq>
\t\t<priority>0.7</priority>
\t</url>""")

cat_sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(cat_sitemap_urls)}
</urlset>"""

with open(os.path.join(BASE_DIR, "category-sitemap.xml"), "w", encoding="utf-8") as fp:
    fp.write(cat_sitemap)
print("✓ Created category-sitemap.xml")

# Generate sitemap.xml (Comprehensive full sitemap)
all_urls = page_sitemap_urls + cat_sitemap_urls + post_sitemap_urls
full_sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(all_urls)}
</urlset>"""

with open(os.path.join(BASE_DIR, "sitemap.xml"), "w", encoding="utf-8") as fp:
    fp.write(full_sitemap)
print("✓ Created sitemap.xml")

# Generate sitemap_index.xml
sitemap_index = f"""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
\t<sitemap>
\t\t<loc>{DOMAIN}/post-sitemap.xml</loc>
\t\t<lastmod>{TODAY}</lastmod>
\t</sitemap>
\t<sitemap>
\t\t<loc>{DOMAIN}/page-sitemap.xml</loc>
\t\t<lastmod>{TODAY}</lastmod>
\t</sitemap>
\t<sitemap>
\t\t<loc>{DOMAIN}/category-sitemap.xml</loc>
\t\t<lastmod>{TODAY}</lastmod>
\t</sitemap>
</sitemapindex>"""

with open(os.path.join(BASE_DIR, "sitemap_index.xml"), "w", encoding="utf-8") as fp:
    fp.write(sitemap_index)
print("✓ Created sitemap_index.xml")


# 3. Fix Missing H1 Tags on index.html, page/2/index.html, page/3/index.html
h1_map = {
    "index.html": "Rojgaro - Information related to Trusted Latest Jobs and Career.",
    "page/2/index.html": "Rojgaro - Information related to Trusted Latest Jobs and Career - Page 2",
    "page/3/index.html": "Rojgaro - Information related to Trusted Latest Jobs and Career - Page 3"
}

for rel_path, h1_text in h1_map.items():
    file_path = os.path.join(BASE_DIR, rel_path)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as fp:
            c = fp.read()
        
        # If no h1 in file, insert semantic hidden H1 inside navigation-branding or main
        if "<h1" not in c:
            h1_html = f'<h1 class="screen-reader-text">{h1_text}</h1>\n'
            # Insert right after <main id="main" class="site-main">
            if '<main id="main" class="site-main">' in c:
                c = c.replace('<main id="main" class="site-main">', '<main id="main" class="site-main">\n        ' + h1_html, 1)
            elif '<div class="navigation-branding">' in c:
                c = c.replace('<div class="navigation-branding">', '<div class="navigation-branding">\n      ' + h1_html, 1)
            
            with open(file_path, "w", encoding="utf-8") as fp:
                fp.write(c)
            print(f"✓ Added SEO H1 tag to {rel_path}")

print("\nAll SEO requirements implemented successfully!")
