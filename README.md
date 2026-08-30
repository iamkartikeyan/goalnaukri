# Goal Naukri (goalnaukri.com) - Exact Website Clone

This repository contains a **1:1 pixel-perfect exact replica** of [Goal Naukri](https://goalnaukri.com/) — Trusted source for Latest Jobs, Admissions, and Career Guidance in Hindi.

---

## 🚀 Features

- **Exact UI & UX**: 100% fidelity to the original GeneratePress + GenerateBlocks theme layout, color palettes (Navy `#020953`, accent blue `#1b78e2`), typography (Open Sans), card styling, and footer design.
- **Complete Page Catalog**:
  - **Home**: Featured article feeds, pagination (Page 1, 2, 3), sidebar with instant search, trending posts thumbnails, Join WhatsApp & Telegram channel CTA buttons.
  - **Category Archives**: `/category/career-guide/`
  - **Legal & Info Pages**: `/about-us/`, `/contact-us/`, `/disclaimer/`, `/privacy-policy/`, `/term-and-conditions/`
  - **Full Article Guides**: 10+ full in-depth Hindi guides with complete tables, eligibility, syllabus, salary breakdowns, author bio boxes, and related posts.
- **Fully Responsive**: Mobile hamburger navigation drawer, adaptive grid columns, tablet/desktop layouts.
- **Interactive JS**: Live client-side instant article search filter, contact form submit confirmation, newsletter feedback, smooth floating back-to-top button.
- **Zero Broken Links / Missing Assets**: All 400+ high-res images, icons, thumbnails, and stylesheets are locally bundled and served for lightning-fast load times.

---

## 🛠️ Local Development

To run locally:
```bash
# Clone the repository
git clone https://github.com/iamkartikeyan/goalnaukri.git
cd goalnaukri

# Start local server
npx serve . -p 8080
# OR
python3 -m http.server 8080
```
Open [http://localhost:8080](http://localhost:8080) in your browser.

---

## 🌐 Deploy to Vercel

```bash
vercel --prod
```
The project includes `vercel.json` with static asset caching headers and clean URL routing out of the box.
