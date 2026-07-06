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

### 2026-07-02 (Thursday · 第 8 期)
- 8th scheduled run. history.json had 36 entries (6/26-7/01 × 6); appended 6 new URLs (total 42). last_updated set to 2026-07-02.
- Newswise Cloudflare block + 2 PSU redirects — gopsusports.com 404 on Levi Haines article (used Onward State mirror). ACSA arch article needed since iee.psu.edu already had La Porta in 7/1 set.
- All 6 images successfully extracted (4 psu-gatsby-files S3, 1 cdn.onwardstate.com, 1 acsa-arch wp-content).
- News selected for 2026-07-02:
  - #1 传媒学院: Bellisario 学院 5 个高中夏令营 7/5-10 (psu.edu, 1/20)
  - #2 演出预告: Palmer 美术馆开馆美国 250 周年当代艺术评审展 (psu.edu, 6/13) — **正好 250 周年社区日 7/2 开馆**
  - #3 校友活动: 校友会欢迎 14 名新领导 7/1 上任三年任期 (psu.edu, 7/1) — **happens yesterday**
  - #4 体育动态: Levi Haines (摔跤) + Tessa Janecke (女冰) 获 Big Ten 荣誉勋章 (Onward State, 6/25)
  - #5 行政人事: Pinto Duarte 出任建筑系临时系主任 (ACSA, 6/10)
  - #6 科研成果: IST 终身副教授 Aron Laszka 获 2026 NSF CAREER 奖 (psu.edu IST, 4/29)
- Files: index.html (title→7/02, date→7/02 星期四, 6 cards replaced, lead-cn updated, stats fixed to 1/1/1/1/1/1), psu-news-2026-07-02.html (new), archive.html (7→8 期, new card top of June section), archive-catalog.html (counts: 7→8, 7→8, 7→8, 9→10, 7→8, 5→6; new item on top of each category).
- Git: 5 files, +1274/-56, commit `545828b`, push c54eba3→545828b.
- **Stream timeout recovered**: terminal output cut off during archive-catalog edit; restarted, verified all files updated, completed git push, memory writes.

### 2026-07-03 (Friday · 第 9 期)
- 9th scheduled run. Manually triggered (8:00 AM cron missed). history.json had 42 entries (6/26-7/02 × 6); appended 6 new URLs (total 48). last_updated set to 2026-07-03.
- **science.psu.edu og:image pattern**: science.psu.edu uses `ecos-appdev-production.s3.amazonaws.com/science_site/s3fs-public/styles/<style>/...` instead of the standard PSU gatsby-files S3. No `og:image` meta tag — image lives in `<div class="story__hero-image-media"><img src="...">`. The `f_story_hero` style returns 2340x900 (close to 16:9). For 16:9 1000w, try `styles/16_9_1000w/...` substitution.
- **Penn State Outreach news is a goldmine for admin slot**: `psu.edu/news/office-vice-president-commonwealth-campuses/...` is a separate index from `/news/administration/`. John Nauright dean announcement lived there (5/15, with og:image).
- **Lee Ahern TLT Award (faculty-and-staff)**: perfect comm slot — Bellisario 学院教师获奖，`/news/faculty-and-staff/...` URL pattern. og:image is psu-gatsby-files 16:9 1000w style.
- **Previous-version content retry**: Palmer "Dreaming American Futures" image (used on 7/2) came up in initial og:image for Arts Festival Images 2026 — replaced with `Huber_000022_079816_936262_14928-953x1024.jpg` from `seeing_america.php` page (it's the dedicated Photos page for the Central PA Arts Festival exhibit).
- **Bustinza CEO announcement (5/18) was previously on 7/1 as "Corner Room 100"** — realized during review that the Bustinza article was already used 7/1 in some form. Verified the actual title_cn diff is OK: 7/1 used "州学院地标 The Corner Room 7 月 3 日办 Corner Fest 街区聚会" while 7/3 uses "Reggie Bustinza 7 月 6 日正式履新 Penn State 校友会 CEO" — distinct topics, no conflict. The 7/1 entry is at a different URL (`alumni.psu.edu/2026/06/11/...`) so no actual URL collision.
- News selected for 2026-07-03:
  - #1 传媒学院: Lee Ahern 获 TLT Impact Award, AI 时代新闻教育 (faculty-and-staff, 3/18)
  - #2 演出预告: Arts Festival Images 2026 摄影展 Schlow Library 7/1-31 (arts-festival.com, 7/1)
  - #3 校友活动: Reggie Bustinza 7/6 履新校友会 CEO (alumni-association, 5/18)
  - #4 体育动态: Dhillon McGee 2027 届德州角卫承诺 (SI, 6/26)
  - #5 行政人事: John Nauright 出任 University College 首任常驻院长 (office-vice-president-commonwealth-campuses, 5/15)
  - #6 科研成果: Nitin Samarth 当选 AAAS 院士 (science.psu.edu, 4/22)
- All 6 images successfully extracted (5 psu-gatsby-files S3, 1 arts-festival wp-content, 1 ecos-appdev-production S3).
- Files: index.html (title→7/03, date→7/03 星期五, 6 cards replaced, lead-cn updated, stats fixed to 1/1/1/1/1/1), psu-news-2026-07-03.html (new), archive.html (8→9 期, new card top of June section), archive-catalog.html (counts: 8→9, 8→9, 8→9, 10→11, 8→9, 6→7; new item on top of each category).
- Git: 6 files, +1306/-57, commit `c230801`, push 545828b→c230801.
- **Manual run note**: User prompted "今天是不是没更新" → I confirmed 7/3 was missing → user "对啊，每天都要更新的" → executed the 9-step automation manually instead of waiting for 8 AM cron. Pattern: when user reports missing day, treat as backfill/execute-now.
- **Today's lead-cn**: "聚焦传媒学院 · 校友领袖 · 体育招生 · 行政任命 · 科研成果" — emphasizes themes rather than category list.

### 2026-07-04 ~ 2026-07-06 (3-day backfill · 第 10-12 期)
- **3-day backfill (周末 + 周一)**. history.json had 48 entries (6/26-7/03 × 6); appended 18 new URLs (total 66). last_updated set to 2026-07-06.
- **Why 3 days missed**: pmset 错配 7/3 设成 07:55 关机（用户把 19:55 改成 07:55）→ 7/4 7:55 / 7/5 7:55 / 7/6 7:55 每天早上自动关机，8:00 cron 全部错过。
- **iMac 7/6 中午 12:02 手动开机**，用户让我重设 6:30 wake + 8:00 shutdown + 7:00 cron 替代 8:00 cron。
- **同时把 WorkBuddy automation RRULE 改为 BYHOUR=7;BYMINUTE=0**（用户问"是否已改成 7 点"，已确认修改成功）。
- **"Reminder 重复"模式延续**（Bustinza 6/29 → 7/3 模式）：4 个"老文章不同角度回顾"在 7/5、7/6 出现：
  - 7/5 #1 传媒: Emily Metzgar 院长上任满一周（4/1 文章，title 改"6 位副院长组队"角度）
  - 7/5 #2 演出: Rhapsody 系列 8/30 揭幕（6/20 文章，title 改"6 场室内乐系列"角度）
  - 7/5 #3 校友: 荣誉校友奖 6/12 颁奖回顾（6/12 文章，title 加"Jain+De Moraes"等获奖人）
  - 7/6 #2 演出: 第 60 届中央宾州艺术节 7/8-12 提醒（6/28 文章，title 改"本周末开幕"角度）
- **4 个全新 7/4 文章**：Hearst 奖 top-10 全部 6 类别 + Ella Langley BJC 9/11 巡演 + Firecracker 4K 跑步 + adidas 替代 Nike 32 年合作。
- **7/6 校友 Dan Barefoot (冬奥钢架雪车)**：从 alumni.psu.edu/spotlight/...（404）改用 psu.edu/news/arts-and-architecture/.../landscape-architecture-alum-competes-skeleton-team-usa-2026-olympics（HTTP 200, og:image 验证通过）。
- **7/6 行政 Daniel Barkowitz (学生援助 AVP)**：Faculty Senate pass-fail 文章没 og:image，改用 `/news/administration/.../penn-state-names-new-assistant-vice-president-executive-director-student-aid`（HTTP 200, og:image `daniel-headshot-5.jpg`）。
- **zsh `status` reserved**：shell 变量名 `status` 在 zsh 是 read-only，`code=$(curl ... -w '%{http_code}')` 才能用。
- News selected:
  - **7/4 第 10 期**: Hearst Top-10 全部 6 类别 / Ella Langley 9/11 BJC / Firecracker 4K / adidas 替换 Nike / Pennington AAUA / 超导钻石量子
  - **7/5 第 11 期**: Metzgar 院长上任一周 / Rhapsody 8/30 揭幕 / 荣誉校友奖 6/12 / 男篮 2026-27 阵容 / Mauro 临时院长 EMS / 生物泵数据存储
  - **7/6 第 12 期**: Ed Bradley 奖学金 2 入选 / 中央艺术节 60 周年开幕提醒 / Dan Barefoot 冬奥钢架雪车 / $10 亿体育收入 / Barkowitz AVP 学生援助 / OCIP 创业商业化
- All 18 images successfully extracted (16 psu-gatsby-files S3, 1 imagedelivery.net generic Firecracker, 1 local21news.com)。
- Files: index.html (title→7/06, date→7/06 星期一, 6 cards replaced, lead-cn updated), psu-news-2026-07-04/05/06.html (3 new files), archive.html (9→12 期, 3 new cards top of June section), archive-catalog.html (counts: 9→12, 9→12, 9→12, 11→14, 9→12, 7→10; 3 new items top of each category).
- Git: 7 files, +3710/-60, commit `24c9a03`, push 53247cf→24c9a03.
- **后处理发现并修复 1 个小 bug**：archive.html 写完后，初始 index.html `<title>` 忘改 7/3→7/6（commit 后才注意到），后续一次性修复补 commit。
