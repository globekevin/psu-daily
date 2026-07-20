# PSU Daily News Project · Long-term Notes

## Project Overview
- **Project**: Penn State University 每日新闻日报 (PSU Daily News)
- **Workspace**: `/Users/mac/WorkBuddy/2026-06-25-12-43-57/psu-news-daily/`
- **Owner**: 凯子鱼
- **Publishing**: GitHub Pages at `https://globekevin.github.io/psu-daily/`
- **Original Automation**: `automation-1782380865203` (now **PAUSED** — replaced by GitHub Actions)

## File Layout
- `index.html` — Main daily landing page
- `psu-news-YYYY-MM-DD.html` — Per-day archive pages
- `archive.html` — All past editions, chronological; insert before `<!-- AUTO-APPEND-MARKER -->`
- `archive-catalog.html` — Categorical index (cat IDs: `cat-传媒学院`, `cat-演出预告`, `cat-校友活动`, `cat-体育动态`, `cat-行政人事`, `cat-科研成果`)
- `history.json` — URL dedup list (`shown_news_history` array)
- `build_auto.py` — GitHub Actions auto-build script (Bing Search + DeepSeek)
- `.github/workflows/daily-build.yml` — CI schedule (UTC 23:00 = Beijing 7:00 AM)

## GitHub Actions Automation (NEW — 2026-07-20)
- **Workflow**: `.github/workflows/daily-build.yml` — cron `0 23 * * *` (UTC) + `workflow_dispatch`
- **Script**: `build_auto.py` — Bing Search API → find articles → fetch content → DeepSeek summary → build all HTML
- **Secrets needed in GitHub repo**: `BING_API_KEY`, `DEEPSEEK_API_KEY`
- **Bing API free tier**: 1,000 searches/month — we use ~6/day = ~180/month
- **DeepSeek model**: `deepseek-chat`, ~$0.001/1K tokens — estimated ~$0.02/day
- **Requirements**: `requirements.txt` (just `requests`)

## Core Conventions

### 6-Category Structure (MANDATORY order)
1. 传媒学院 (Bellisario College) — mandatory
2. 演出预告 (events/art)
3. 校友活动 (alumni)
4. 体育动态 (sports/recruiting)
5. 行政人事 (admin appointments, deans, policies)
6. 科研成果 (research, science) — mandatory

### Image Handling (CRITICAL — 2026-07-20 triple-redundancy)
- **Inline `style="opacity:1"` on every img tag** — bypasses CSS cache issues
- **CSS default `opacity: 1`** — fail-safe
- **JS check**: `naturalWidth === 0` for broken images
- **Image sources**: PSU Gatsby CDN (`psu-gatsby-files-prod.s3.amazonaws.com`), SI/Minute Media CDN (`images2.minutemediacdn.com`), Eberly Science CDN (`ecos-appdev-production.s3.amazonaws.com`)
- **Avoid**: Gannett CDN (`usatoday.com/gcdn/`) — returns 406

### URL Dedup
Check against ALL URLs in `history.json` `shown_news_history` array before using.

### JSON Quote Safety
- NEVER raw `"` in `title_cn` — use `"`/`"` (Chinese curly quotes)
- Verify: `python3 -c "import json; json.load(open('history.json'))"`

### Git Workflow
Commit: `Daily news update YYYY-MM-DD: <keywords>` → push to `origin main`

### Design System
- `--psu-navy: #001E44`, `--psu-navy-light: #1E4079`, `--psu-gold: #B5995E`
- Category tag colors: 传媒=red, 演出=navy, 校友=purple, 体育=gold, 行政=green, 研究=blue
- Mobile: `html, body { overflow-x: hidden; max-width: 100%; }` + grid children `min-width: 0`
- Footer: Accordion pattern — `aria-expanded` + `hidden` attribute (works without JS)
- Source badge classes: `psu` (navy), `onward` (orange), `collegian` (purple) — combine in single `class` attr, never double

## Anti-Scraping Notes
- Onward State / Collegian / StateCollege.com: Cloudflare → prefer SI mirror or psu.edu source
- Gannett CDN: 406 on all requests → use SI Minute Media CDN instead
- Bing Search API: works reliably from GitHub Actions (no Cloudflare for search results)

## Past Manual Triggers
- 2026-06-29 (aborted cron; re-run manually)
- 2026-07-03 (8 AM cron missed; manual)

## iMac Power Schedule (legacy — replaced by GitHub Actions)
- Wake: 6:40 AM, Shutdown: 8:30 AM
- `sudo pmset repeat wakeorpoweron MTWRFSU 06:40:00 shutdown MTWRFSU 08:30:00`
