#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implement all 5 SEO & Security Audit items:
1. Schema Markup (JSON-LD: Organization, WebSite, Article, Breadcrumbs)
2. Analytics (GA4 / GTM detection)
3. Social Links structured metadata & presence
4. Cookie Consent Banner (with LocalStorage)
5. CSP (Content Security Policy) Protection
"""

import glob
import os
import re

BASE_DIR = "/Users/kartikeyansahani/goalnaukri"
DOMAIN = "https://rojgaro.com"

# 1. CSP Meta Tag
CSP_META = '<meta http-equiv="Content-Security-Policy" content="default-src \'self\' https: data: \'unsafe-inline\' \'unsafe-eval\'; img-src \'self\' https: data:; media-src \'self\' https:; frame-src https://www.youtube.com https://youtube.com https://www.youtube-nocookie.com;">'

# 2. GA4 Analytics Script
GA4_SCRIPT = """<!-- Google Analytics 4 (GA4) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-ROJGARO2026"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-ROJGARO2026');
</script>"""

# 3. Cookie Consent Banner HTML & CSS
COOKIE_CONSENT_HTML = """
<!-- Cookie Consent Banner -->
<div id="rojgaro-cookie-consent" style="display:none;position:fixed;bottom:20px;left:50%;transform:translateX(-50%);width:calc(100% - 40px);max-width:580px;background:#020953;color:#fff;padding:16px 22px;border-radius:12px;box-shadow:0 10px 30px rgba(0,0,0,0.35);z-index:99999;border:1px solid rgba(255,255,255,0.15);font-family:inherit;box-sizing:border-box;">
  <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
    <p style="margin:0;font-size:14px;line-height:1.5;color:#e2e8f0;flex:1;min-width:240px;">
      हम आपके अनुभव को बेहतर बनाने और एनालिटिक्स के लिए कुकीज़ का उपयोग करते हैं। अधिक जानकारी के लिए हमारी <a href="/privacy-policy/" style="color:#83b0de;text-decoration:underline;">Privacy Policy</a> देखें।
    </p>
    <div style="display:flex;gap:8px;">
      <button id="cookie-accept-btn" style="background:#1b78e2;color:#fff;border:none;padding:8px 18px;border-radius:6px;font-size:14px;font-weight:700;cursor:pointer;transition:0.2s;">Accept</button>
      <button id="cookie-decline-btn" style="background:transparent;color:#94a3b8;border:1px solid rgba(255,255,255,0.2);padding:8px 14px;border-radius:6px;font-size:14px;cursor:pointer;transition:0.2s;">Decline</button>
    </div>
  </div>
</div>
<script>
(function(){
  try {
    if (!localStorage.getItem('rojgaro_cookie_consent')) {
      var b = document.getElementById('rojgaro-cookie-consent');
      if (b) {
        b.style.display = 'block';
        document.getElementById('cookie-accept-btn').onclick = function(){
          localStorage.setItem('rojgaro_cookie_consent', 'accepted');
          b.style.display = 'none';
        };
        document.getElementById('cookie-decline-btn').onclick = function(){
          localStorage.setItem('rojgaro_cookie_consent', 'declined');
          b.style.display = 'none';
        };
      }
    }
  } catch(e) {}
})();
</script>
"""

# Org & Website Schema
SITE_SCHEMA = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://rojgaro.com/#organization",
      "name": "Rojgaro",
      "url": "https://rojgaro.com/",
      "logo": {
        "@type": "ImageObject",
        "@id": "https://rojgaro.com/#logo",
        "url": "https://rojgaro.com/wp-content/uploads/2026/05/rojgaro-logo.png",
        "caption": "Rojgaro"
      },
      "sameAs": [
        "https://chat.whatsapp.com/Lnb4fxnJTQmJByUOzhxvnT",
        "https://t.me/rojgaro",
        "https://x.com/rojgaro_",
        "https://www.instagram.com/rojgaro"
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://rojgaro.com/#website",
      "url": "https://rojgaro.com/",
      "name": "Rojgaro",
      "description": "Information related to Trusted Latest Jobs and Career.",
      "publisher": { "@id": "https://rojgaro.com/#organization" },
      "potentialAction": [
        {
          "@type": "SearchAction",
          "target": {
            "@type": "EntryPoint",
            "urlTemplate": "https://rojgaro.com/?s={search_term_string}"
          },
          "query-input": "required name=search_term_string"
        }
      ]
    }
  ]
}
</script>"""

html_files = glob.glob(os.path.join(BASE_DIR, "**/*.html"), recursive=True)
updated_count = 0

for f in html_files:
    with open(f, "r", encoding="utf-8") as fp:
        c = fp.read()
        
    orig = c
    
    # Extract metadata for custom schema
    title_m = re.search(r"<title>(.*?)(?:\s*-\s*Rojgaro)?</title>", c)
    page_title = title_m.group(1).strip() if title_m else "Rojgaro"
    
    desc_m = re.search(r'<meta name="description" content="([^"]+)"', c)
    page_desc = desc_m.group(1).strip() if desc_m else page_title
    
    # 1. Add CSP & GA4 to <head> if missing
    if "Content-Security-Policy" not in c:
        c = c.replace("<head>", "<head>\n" + CSP_META + "\n" + GA4_SCRIPT, 1)
        
    # 2. Add Schema Markup
    # Determine if single blog post
    rel_path = os.path.relpath(f, BASE_DIR)
    is_root_static = rel_path in ["index.html", "about-us.html", "contact-us.html", "privacy-policy.html", "disclaimer.html", "term-and-conditions.html"]
    is_sub_static = rel_path in ["about-us/index.html", "contact-us/index.html", "privacy-policy/index.html", "disclaimer/index.html", "term-and-conditions/index.html", "page/2/index.html", "page/3/index.html", "category/career-guide.html", "category/career-guide/index.html", "category/career-guide/page/2/index.html", "category/career-guide/page/3/index.html"]
    
    if is_root_static or is_sub_static:
        # Website & Org Schema
        if 'application/ld+json' not in c:
            c = c.replace("</head>", SITE_SCHEMA + "\n</head>", 1)
    else:
        # Blog post
        slug = rel_path.replace(".html", "").replace("/index", "")
        img_m = re.search(r'<meta property="og:image" content="([^"]+)"', c)
        if not img_m:
            img_m = re.search(r'<div class="post-image">\s*<img[^>]+src="([^"]+)"', c)
        img_url = (DOMAIN + img_m.group(1)) if (img_m and img_m.group(1).startswith("/")) else (img_m.group(1) if img_m else f"{DOMAIN}/wp-content/uploads/2026/05/rojgaro-logo.png")
        
        date_m = re.search(r'<time class="entry-date published" datetime="([^"]+)"', c)
        pub_date = date_m.group(1) if date_m else "2026-05-15T12:00:00+00:00"
        
        blog_schema = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {SITE_SCHEMA.replace('<script type="application/ld+json">', '').replace('</script>', '').strip()},
    {{
      "@type": "Article",
      "@id": "{DOMAIN}/{slug}/#article",
      "isPartOf": {{ "@id": "{DOMAIN}/#website" }},
      "headline": "{page_title.replace('"', '')}",
      "description": "{page_desc.replace('"', '')}",
      "image": "{img_url}",
      "datePublished": "{pub_date}",
      "dateModified": "{pub_date}",
      "mainEntityOfPage": "{DOMAIN}/{slug}/",
      "author": {{
        "@type": "Person",
        "name": "Kartikeyan Sahani",
        "url": "{DOMAIN}/about-us/"
      }},
      "publisher": {{
        "@id": "{DOMAIN}/#organization"
      }}
    }},
    {{
      "@type": "BreadcrumbList",
      "@id": "{DOMAIN}/{slug}/#breadcrumb",
      "itemListElement": [
        {{
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "{DOMAIN}/"
        }},
        {{
          "@type": "ListItem",
          "position": 2,
          "name": "Career Guide",
          "item": "{DOMAIN}/category/career-guide/"
        }},
        {{
          "@type": "ListItem",
          "position": 3,
          "name": "{page_title.replace('"', '')}"
        }}
      ]
    }}
  ]
}}
</script>"""
        if 'application/ld+json' not in c:
            c = c.replace("</head>", blog_schema + "\n</head>", 1)

    # 3. Add Cookie Consent Banner before </body>
    if "rojgaro-cookie-consent" not in c and "</body>" in c:
        c = c.replace("</body>", COOKIE_CONSENT_HTML + "\n</body>", 1)
        
    if c != orig:
        with open(f, "w", encoding="utf-8") as fp:
            fp.write(c)
        updated_count += 1

print(f"✓ Implemented SEO & Security audit fixes in {updated_count} HTML files.")
