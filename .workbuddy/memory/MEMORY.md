# PSU Daily News Project · Long-term Notes

## Project Overview
- **Project**: Penn State University 每日新闻日报 (PSU Daily News)
- **Workspace**: `/Users/mac/WorkBuddy/2026-06-25-12-43-57/psu-news-daily/`
- **Owner**: 凯子鱼 (Buddy compiles on his behalf)
- **Publishing**: GitHub Pages at `https://globekevin.github.io/psu-daily/`
- **Automation**: Scheduled daily at 8:00 AM (RRULE `FREQ=DAILY;BYHOUR=8;BYMINUTE=0`)
- **Automation ID**: `automation-1782380865203`

## File Layout
- `index.html` — Main daily landing page (today's 6 news)
- `psu-news-YYYY-MM-DD.html` — Per-day archive pages (one per edition)
- `archive.html` — All past editions, chronological list
- `archive-catalog.html` — Categorical index (6 categories: 传媒学院/演出预告/校友活动/体育动态/行政人事/科研成果)
- `history.json` — Shown-news dedup list (`shown_news_history` array, `last_updated` field)
- `.workbuddy/automations/automation-1782380865203/memory.md` — Automation execution log
- `.workbuddy/memory/YYYY-MM-DD.md` — Daily project work log

## Core Conventions

### 1. The 6-Category Structure
Every day picks **exactly 6 news items**, one per category, in this order:
1. 传媒学院 (Bellisario College) — MANDATORY
2. 演出预告 (events/art)
3. 校友活动 (alumni)
4. 体育动态 (sports; may be recruiting/policy/awards)
5. 行政人事 (admin appointments, deans, policies)
6. 科研成果 (research, science) — MANDATORY

### 2. Image Fetching (CRITICAL)
- **Primary method**: `curl -s -L -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" "<url>" -o /tmp/x.html && grep -oE '<meta property="og:image" content="[^"]+"' /tmp/x.html`
- **Always verify the image actually exists** by opening the URL.
- **PSU gatsby-files URL pattern** (most common): `https://psu-gatsby-files-prod.s3.amazonaws.com/s3fs-public/styles/16_9_1000w/public/<year>/<month>/<filename>.jpg?h=<hash>&itok=<token>`
- **SI / Onward State / College media** use `images2.minutemediacdn.com/image/upload/...` (Imagn CDN) or `cdn.onwardstate.com/uploads/...`
- **science.psu.edu exception**: uses `ecos-appdev-production.s3.amazonaws.com/science_site/s3fs-public/styles/<style>/...` and has NO `og:image` meta tag — image is in `<div class="story__hero-image-media">` directly
- **mri.psu.edu articles lack og:image** — use in-body `<img src="...">` if no choice, or skip

### 3. Image Fallback
If no unique og:image, skip the article. Always have backup candidates.

### 4. URL Dedup
Before committing any new URL, verify against `history.json` `shown_news_history` array. Last 12-18 entries are most important (within 2-3 days).

### 5. JSON Quote Safety
- **NEVER** write raw `"` (English double quote) inside any `title_cn` value
- Always use `"`/`"` (Chinese curly quotes) or `「」` for quotation marks
- After editing, verify with: `python3 -c "import json; json.load(open('history.json'))"`

### 6. Git Workflow
- `git add history.json index.html archive.html archive-catalog.html psu-news-YYYY-MM-DD.html .workbuddy/memory/YYYY-MM-DD.md`
- Commit message: `Daily news update YYYY-MM-DD: <keyword1>, <keyword2>, ...`
- Push to `origin main` (auto-deploys to GitHub Pages)

## File Update Patterns

### index.html updates
- `<title>` line: change date
- `id="todayDate"` div: change "YYYY年M月D日 星期X"
- `.lead-cn` div: replace with today's themes
- 6 news cards (entire `<article class="news-card" id="news-1">` ... `id="news-6">`)
- `history.json` last_updated field

### archive.html
- Prepend new card BEFORE the `<!-- AUTO-APPEND-MARKER - DO NOT REMOVE -->` comment
- Update `共 N 期` count (N+1)

### archive-catalog.html
- For each of 6 `cat-section` blocks:
  - Update count (X → X+1)
  - Prepend new `<a class="news-item">` entry to the top of `news-list`

### psu-news-YYYY-MM-DD.html (new file)
- `cp` from previous day's file
- Edit 4 places: `<title>`, todayDate div, edition number, lead-cn/lead-en
- Replace all 6 news cards

## Past Manual Triggers
- 2026-06-29 (was aborted cron; user prompted re-run)
- 2026-07-03 (8:00 AM cron missed; user reported, executed manually)

## Cloudflare & Anti-Scraping Workarounds
- **Onward State / Collegian / StateCollege.com**: blocked by Cloudflare → use SI mirror or alternative source
- **Newswise**: blocked → use original PSU source (psu.edu/news/...) directly
- **WebFetch tool**: unreliable, prefer curl

## Design System (PSU Brand)
- `--psu-navy: #041E42` (Nittany Navy)
- `--psu-navy-light: #1E407C` (Penn State Blue)
- `--psu-gold: #FFC72C` (Penn State Gold)
- Category tag colors: 传媒=red, 演出=navy, 校友=purple, 体育=gold, 行政=green, 研究=blue

## Index Page Stats
4 stat cards: 今日精选 (6), 传媒学院 (1), 演出预告 (1), 体育动态 (1) — note: only 3 categories shown, but the 6-card grid has all 6.
