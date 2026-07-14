# PSU Daily News Project · Long-term Notes

## Project Overview
- **Project**: Penn State University 每日新闻日报 (PSU Daily News)
- **Workspace**: `/Users/mac/WorkBuddy/2026-06-25-12-43-57/psu-news-daily/`
- **Owner**: 凯子鱼 (Buddy compiles on his behalf)
- **Publishing**: GitHub Pages at `https://globekevin.github.io/psu-daily/`
- **Automation**: Scheduled daily at 7:00 AM (RRULE `FREQ=DAILY;BYHOUR=7;BYMINUTE=0`)
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

## iMac Power Schedule
- **开机**: 每天 6:40 AM (`wakepoweron` — 自动开机/唤醒)
- **关机**: 每天 8:30 AM (`shutdown`)
- **自动化触发**: 每天 7:00 AM（在开机和关机之间）
- **缓冲**: 开机后有 20 分钟系统准备时间；任务执行窗口最长 1 小时 30 分钟
- **设置命令**: `sudo pmset repeat wakeorpoweron MTWRFSU 06:40:00 shutdown MTWRFSU 08:30:00`
- ⚠️ 调整原因：原 6:55-8:00 窗口过紧，开机仅 5 分钟缓冲导致 7/9 漏触发

## Mobile Responsive — Required CSS (added 2026-07-14)
**User reported**: iPhone 13 Pro 截图显示页面底板超出屏幕宽度，左右滑动露出黑色背景。

**Root cause**: 微信 WebView viewport 报告不可靠（"请求桌面版"或缩放状态），原本期望触发的 `@media (max-width: 429px)` 没生效，按桌面布局渲染；同时 `html/body` 没有 `overflow-x:hidden` 兜底，导致任何子元素（toc-inner、stats、sources、footer 网格）都能把 body 撑宽。

**Mandatory CSS for all daily pages** (top of style block, after `*` reset):
```css
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
html, body {
  overflow-x: hidden;
  max-width: 100%;
  width: 100%;
}
body {
  ...
  -webkit-text-size-adjust: 100%;
}
.news-grid, .sources-grid, .stats, .footer-grid, .toc-inner, .header-main {
  min-width: 0;  /* prevent intrinsic min-content overflow */
}
.card-summary { word-break: break-word; overflow-wrap: break-word; }
```

**HTML bug to watch for in build script** (fixed in `build_20260714.py` line 152):
- ❌ `<span{source_class} class="source-badge">` produces **two `class` attributes** (browser uses only first, breaking styles)
- ✅ Combine into single attribute: `classes = ["source-badge"]; [classes.insert(0, c) for c in source_class.split()]; f' class="{" ".join(classes)}"'`
- This bug existed in 5 source-badge spans per day → daily pages before 2026-07-14 all have it

**Files fixed in commit c7a57d6**: `index.html`, `psu-news-2026-07-14.html`, `build_20260714.py`.
