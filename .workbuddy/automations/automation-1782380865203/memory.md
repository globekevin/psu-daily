# PSU Daily News Automation Memory

## Execution History

### 2026-06-26 (First Run)
- Initial automation run. history.json did not exist, created fresh.
- Selected 6 news items covering all 6 categories.
- Updated index.html, archive.html, archive-catalog.html.
- Created psu-news-2026-06-26.html archive page.
- Git push successful: 26d59a2.
- News: Emily Metzgar dean appointment (comm), Arboretum papermaking (events), Homecoming 2026 theme (alumni), Dhillon McGee commitment (recruiting), NCAA 5-year eligibility rule (policy), Beaver Stadium renovation topping out (admin/campus dev).
- **Content dedup rule added** to automation prompt after #6 was found to duplicate #1 (same Metzgar story). Replaced with Beaver Stadium renovation news (e5e9e3b).
- **Image support added (d957045)**: Each news card now has an optional `.card-image` div after the title-en line. CSS includes responsive sizes (desktop 280px → tablet 240px → phone 200px → small 150px) and dark mode support. The `onerror` handler auto-hides the div when no image is available. Automation prompt updated with image fetching instructions (Step 3: scrape og:image from each article).

### 2026-06-26 (Image Mobile Adaptation - ddb4dbc)
- **Improved `.card-image` CSS**: Added `aspect-ratio: 16/9` to prevent layout shift (CLS) during image loading. Background gradient provides a loading placeholder.
- **Added image fade-in animation**: `opacity: 0 → 1` with `transition: opacity 0.4s ease` for smooth appearance.
- **Added JS empty-image handler**: Detects `img[src=""]` and hides the container before layout calculation.
- **All breakpoints covered with image max-height**: Desktop 280px, iPad 240px, foldable inner 240px, iPad Pro landscape 260px, large phone 200px, standard phone 180px, small phone 150px, landscape phone 160px.
- **Fetched and inserted real images** for all 6 news cards today:
  - #1 Emily Metzgar: `psu-gatsby-files...emily-metzgar.jpg`
  - #2 Arboretum: `psu-gatsby-files...papermaking-news-hero-image.png`
  - #3 Homecoming: `homecoming.psu.edu/IMG_9687.jpeg`
  - #4 McGee recruiting: Wikipedia Penn State Nittany Lions logo (fallback)
  - #5 NCAA rule: Chicago Tribune Big Ten image
  - #6 Beaver Stadium: SI.com construction image
- **Dark mode `.card-image` background**: `linear-gradient(135deg, #1a1a2e, #0d0d1a)` for OLED screens.

### 2026-06-27
- Second scheduled run. history.json had 6 entries (6/26); appended 6 new URLs.
- Same Edit/curl pattern as 6/26. Wrote psu-news-2026-06-27.html and pushed as 8378b80.
- News selected:
  - #1 Comm: Luczak 实习系列开篇
  - #2 演出: Hershey 交响乐团"美国颂"6/26
  - #3 校友: We Are Weekend 6/26-27
  - #4 体育: Elijah Guertin 2027 届四星 edge 承诺
  - #5 行政: Brent Scott 晋升副主教练
  - #6 科研: photomemristor 仿人眼 (Nature Comm.)

### 2026-06-28
- Third scheduled run. history.json had 12 entries (6/26 + 6/27); appended 6 new URLs (total 18).
- **WebFetch timed out (30s) on psu.edu, sciencedaily.com, si.com** — fell back to `curl -L -A "Mozilla/5.0 Chrome/120"` to /tmp/*.html + `grep -oE 'og:image[^>]+content="[^"]+"'`. This worked reliably for all targets. Use this as the PRIMARY method going forward, not WebFetch.
- **Discovered SI.com og:image format quirk**: `og:image:width` / `og:image:height` come BEFORE the actual `og:image` content — need to filter them out. Real image URL is on a separate `<meta property="og:image" content="...">` line.
- **Workday article (psu.edu 6/25) has NO unique og:image** — falls back to `/news/images/og-fallback.jpg`. Replaced with "Extended Learning Partnerships rename" (6/24) which has a real ELP wordmark image.
- **PSU outreach articles live at /news/outreach/, not /news/administration/** — admin index lists them too. Use admin index to find slugs.
- News selected for 2026-06-28:
  - #1 Comm: Jeff Brown (CommRadio 创始人) 6/30 退休
  - #2 演出预告: 第 60 届中央宾州艺术节 7/8-12
  - #3 校友活动: "Raise the Bar" 九城巡回系列落幕
  - #4 体育动态: 男篮 Dasonte Bowen 转会"隐藏宝石" (basketball portal pickup, SI)
  - #5 行政人事: Extended Learning Partnerships 更名 (psu.edu/news/outreach, 6/24)
  - #6 科研成果: DNA 修复基因 EXO1 致癌新发现 (sciencedaily → Nature Comm., 6/19)
- All 6 images successfully extracted (3 from psu-gatsby-files S3, 1 SI ImagnImages, 1 arts-festival.com wp-content, 1 sciencedaily.com CDN).
- Files: index.html (title, date, 6 cards), psu-news-2026-06-28.html (new), archive.html (4期, new card top), archive-catalog.html (6 categories each +1, new item on top of each).
- Git: 5 files, +1242/-54, commit `2e2d648`, push 8378b80→2e2d648.

### 2026-06-29
- **Re-run for 6/29** (previous 6/28 scheduled run was aborted — user reported "怎么没有更新新闻"). Today's content shows 6/29 slot rather than 6/28. This is a normal re-run, not a backfill.
- Fifth scheduled edition. history.json had 18 entries (6/26+6/27+6/28); appended 6 new URLs (total 24). last_updated set to 2026-06-29.
- Curl + UA headers worked for all 6 og:images on first try. No WebFetch fallbacks needed.
- News selected for 2026-06-29:
  - #1 Comm: Jocelyn Bilker 暑期赴 NBC News DC 实习 (Bellisario, 6/12)
  - #2 演出预告: 音乐学院 2026-27 Rhapsody "狂想曲" 系列 8/30 揭幕 (Arts & Architecture, 6/20)
  - #3 校友活动: Reggie Bustinza 任校友会新 CEO，7/6 上任 (Alumni Association, 5/18)
  - #4 体育动态: 摔跤选手 Mesenbrink 获 2026 ESPY 提名 (Onward State, 6/28)
  - #5 行政人事: EMS 院长 Lee Kump 6/30 卸任 9 年任期 + 新设校长卓越奖 (iee.psu.edu, 6/29)
  - #6 科研成果: PET 塑料瓶→电池级石墨 (Research, 6/27, Diamond and Related Materials)
- All 6 images successfully extracted (5 psu-gatsby-files S3, 1 cdn.onwardstate.com).
- Files: index.html (title, date, 6 cards), psu-news-2026-06-29.html (new), archive.html (5期, new card top), archive-catalog.html (6 categories each +1, new item on top of each).
- Git: 5 files, +1244/-56, commit `b846ab1`, push 2e2d648→b846ab1.
### 2026-07-01 (Wednesday · 第 7 期)
- 7th scheduled run. history.json had 30 entries (6/26-6/30 × 6); appended 6 new URLs (total 36). last_updated set to 2026-07-01.
- **Newswise Cloudflare block** on `newswise.com/articles/glass-cells-of-atoms-...`. Worked around by going direct to PSU source `/news/materials-research-institute/...` (Nature MN, 6/18).
- **Onward State 404** on `onwardstate.com/2026/06/23/penn-state-football-to-host-23rd-lift-for-life-event-in-july/`. Used SI.com mirror of same story.
- News selected for 2026-07-01:
  - #1 传媒学院: 15 PSU students + AP cover FIFA World Cup Toronto (Bellisario, 6/12)
  - #2 演出预告: Hintzpiration Alumni Center Art Exhibition 7/10-11 (Alumni, 6/18)
  - #3 校友活动: The Corner Room 100th Anniversary Corner Fest 7/3 (Alumni, 6/11)
  - #4 体育动态: 23rd Annual Lift For Life 7/1 (SI, 6/23) — **happens TODAY**
  - #5 行政人事: La Porta named interim Engineering Dean 7/1 (iee.psu.edu, 6/18) — **happens TODAY**
  - #6 科研成果: Glass atomic vapor cells for sensors, Nature MN (PSU+NIST, 6/18)
- All 6 images successfully extracted (4 psu-gatsby-files S3, 1 alumni.psu.edu, 1 SI ImagnImages).
- Files: index.html (title→7/01, date→7/01 星期三, 6 cards replaced), psu-news-2026-07-01.html (new), archive.html (6→7 期, new card top of June section), archive-catalog.html (counts: 6→7, 6→7, 6→7, 8→9, 6→7, 4→5; new item on top of each category).
- Git: 5 files, +1274/-56, commit `c54eba3`, push a35fa2d→c54eba3.
- **Coincidence noted**: Two slots (#4 Lift For Life 7/1, #5 La Porta interim dean 7/1) both have effective dates of "today" (7/1) — first time multiple slots align with the publish day. Worth checking if this timing effect should drive future selection logic.

### 2026-06-30 (Tuesday · 第 6 期)
- 6th scheduled run. history.json had 24 entries (6/26+6/27+6/28+6/29); appended 6 new URLs.
- **history.json bug fixed**: prior runs left unescaped Chinese curly quotes in some `title_cn` values (e.g. `“先行一步”` written as raw `"先行一步"`). Python script rebalanced opening/closing quote positions and replaced inner unescaped `"` with `"`/`"` (Chinese curly quotes). 30 entries now valid JSON.
- News selected for 2026-06-30:
  - #1 传媒学院: Bellisario 副教授 Steve Manuel 6/30 退休（30 年军事摄影 + 30 年教学）— 当天最后一天，timing 完美 (psu.edu/news/bellisario-college-communications, 5/1)
  - #2 演出预告: HUB-Robeson 画廊石井秀德「Feral Botanica」装置展至 10/31 (Student Affairs, 6/5)
  - #3 校友活动: 三位 Penn Stater 获 2026 荣誉校友奖，含 2025 沃尔夫物理学奖得主 Jain (Alumni Association, 6/12)
  - #4 体育动态: 四星 2028 届 OT Eytan D'oleo 力挺 Penn State 招募文化 (Nittany Lions Wire, 6/29)
  - #5 行政人事: Meeghan Hollis 6/1 出任住宿生活高级主任，统管 2 万学生 12 校区 (Student Affairs)
  - #6 科研成果: AI（ChatGPT 等）答健康问题准确率仅 76%，近 1/4 回答存风险 (Research)
- All 6 images successfully extracted (5 psu-gatsby-files S3, 1 nittanylionswire cdn).
- Files: index.html (title→6/30, date→6/30 星期二, 6 cards replaced), psu-news-2026-06-30.html (new), archive.html (5→6 期, new card top), archive-catalog.html (counts: 5→6, 5→6, 5→6, 7→8, 5→6, 3→4; new item on top of each category).
- Git: 5 files, +1277/-65, commit `a35fa2d`, push b846ab1→a35fa2d.
- **Stream timeout recovered**: this run's terminal output was cut off mid-task; restarted from archive.html edit, verified history.json/index.html already updated, completed all remaining steps (archive page, archive-catalog, git push, memory writes).

## Pattern Notes (carry forward)
- **Curl > WebFetch** for og:image extraction. WebFetch is unreliable; curl is fast and predictable.
- **Curl command template**: `curl -s -L -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" "<url>" -o /tmp/x.html`. Add 2-3s sleep between same-domain requests.
- **PSU admin index page** (`/news/administration/`) is the best way to find recent admin slugs — admin index lists 20+ recent articles.
- **Skip articles without unique og:image** (fallback to `/news/images/og-fallback.jpg`). Always have backup candidates.
- **OG image pattern is consistent**: psu.edu articles use `psu-gatsby-files-prod.s3.amazonaws.com/s3fs-public/styles/16_9_1000w/...`; SI uses `images2.minutemediacdn.com/image/upload/...`; ScienceDaily uses `sciencedaily.com/images/1920/...`; **Onward State uses `cdn.onwardstate.com/uploads/...`** (no query/hash suffix).
- **Slot #6 (科研成果) is mandatory** every day. Search "Penn State research news [date] Nature Science" first; if nothing in 7 days, broaden to biotech/AI/medical.
- **history.json quote safety**: NEVER write raw `"` (English double quote) inside any `title_cn` value. Always use `"`/`"` (Chinese curly quotes) or `「」` for quotation marks in Chinese content. Multi-day history will accumulate unescaped quotes and break JSON validation. After editing, run `python3 -c "import json; json.load(open('history.json'))"` to verify.
- **mri.psu.edu articles lack og:image** — they use in-body `<img src="...">` instead. Skip and find psu.edu `/news/research/...` article instead.
- **Doctor GPT / AI health study is a reliable backup research slot** — published late May, well-cited, og:image on psu-gatsby-files S3.
- **Steve Manuel retirement is well-timed** for any June 30 (last working day) — when 6/30 falls on a weekday, this is a perfect slot #1 (Bellisario).
