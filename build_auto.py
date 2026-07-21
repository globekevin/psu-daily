#!/usr/bin/env python3
"""
PSU Daily News Auto-Builder for GitHub Actions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
psu.edu/news 直接抓取 → 按分类精准获取新闻
Onward State + NSN RSS  → 补充体育/校园动态
GitHub Models (GPT-4o-mini) → 免费中文摘要

Zero外部API依赖 — 只需要 GitHub Actions 自带的 GITHUB_TOKEN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Required env vars:
  GITHUB_TOKEN  — GitHub Actions 自动注入，用于 GitHub Models API
"""

import os, sys, json, re, datetime, time, textwrap, hashlib, traceback
import html as html_module
import requests

# ═══════════════════════════════════════════════════
#  CONFIGURATION
# ═══════════════════════════════════════════════════

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GH_MODELS_URL = "https://models.inference.ai.azure.com/chat/completions"

# US Eastern time (Penn State's timezone)
ET = datetime.timezone(datetime.timedelta(hours=-4))
now = datetime.datetime.now(ET)
TODAY = now.strftime("%Y-%m-%d")
TODAY_CN = f"{now.year}年{now.month}月{now.day}日"
WEEKDAYS = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
WEEKDAY = WEEKDAYS[now.weekday()]

BASE = os.path.dirname(os.path.abspath(__file__))

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# ═══════════════════════════════════════════════════
#  6 CATEGORIES — scrape targets
# ═══════════════════════════════════════════════════

CATEGORY_SCRAPE = {
    "传媒学院": [
        "https://www.psu.edu/news/bellisario-college-communications/",
    ],
    "演出预告": [
        "https://www.psu.edu/news/arts-and-architecture/",
        "https://www.psu.edu/news/arts-and-entertainment/",
    ],
    "校友活动": [
        "https://www.psu.edu/news/development-and-alumni-relations/",
    ],
    "行政人事": [
        "https://www.psu.edu/news/administration/",
    ],
    "科研成果": [
        "https://www.psu.edu/news/research/",
        "https://www.psu.edu/news/engineering/",
        "https://www.psu.edu/news/science-and-technology/",
    ],
}

# For 体育动态: use RSS feeds from sports sites
SPORTS_RSS_FEEDS = [
    "https://nittanysportsnow.com/feed/",
    "https://onwardstate.com/feed/",
]

# Also scrape Onward State for general campus news (补演出/校友)
ONWARD_RSS = "https://onwardstate.com/feed/"

CATEGORY_META = {
    "传媒学院": {"id": "news-1", "tag": "tag-comm", "cat_id": "cat-传媒学院", "source": "Penn State News", "source_class": "psu"},
    "演出预告": {"id": "news-2", "tag": "tag-up", "cat_id": "cat-演出预告", "source": "Penn State News", "source_class": "psu"},
    "校友活动": {"id": "news-3", "tag": "tag-alumni", "cat_id": "cat-校友活动", "source": "Penn State News", "source_class": "psu"},
    "体育动态": {"id": "news-4", "tag": "tag-sports", "cat_id": "cat-体育动态", "source": "Nittany Sports Now", "source_class": ""},
    "行政人事": {"id": "news-5", "tag": "tag-admin", "cat_id": "cat-行政人事", "source": "Penn State News", "source_class": "psu"},
    "科研成果": {"id": "news-6", "tag": "tag-research", "cat_id": "cat-科研成果", "source": "Penn State News", "source_class": "psu"},
}

CATEGORY_ORDER = ["传媒学院", "演出预告", "校友活动", "体育动态", "行政人事", "科研成果"]

# ═══════════════════════════════════════════════════
#  UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════

def log(msg):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)

def load_history():
    path = os.path.join(BASE, "history.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    urls = set()
    dates = set()
    for e in data.get("shown_news_history", []):
        urls.add(e.get("url", ""))
        if e.get("date"):
            dates.add(e["date"])
    edition = len(dates) + 1
    return data, urls, edition

def is_dup(url, known_urls):
    return url in known_urls

def url_to_key(url):
    """Normalize URL for dedup (strip trailing slash, www, etc)."""
    url = url.strip().rstrip("/")
    url = re.sub(r"^https?://(www\.)?", "", url)
    return url

# ═══════════════════════════════════════════════════
#  SCRAPE: psu.edu/news category pages
# ═══════════════════════════════════════════════════

def scrape_psu_category(url, max_items=12):
    """
    Scrape a psu.edu/news/{category}/ page.
    Returns list of {title, url, snippet}.
    """
    results = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
        resp.raise_for_status()
        page_html = resp.text
    except Exception as e:
        log(f"  ✗ scrape failed {url}: {e}")
        return results

    # Find all article links: /news/{category}/story/{slug}
    # Pattern: <a ... href="/news/xxx/story/yyy" ...>Title Text</a>
    links = re.findall(
        r'<a\s[^>]*href="(/news/(?:[^/]+/)?story/[^"]+)"[^>]*>([^<]+)</a>',
        page_html
    )

    seen = set()
    for href, title in links:
        full_url = "https://www.psu.edu" + href
        title = title.strip()
        title = html_module.unescape(title)  # Fix &#x27; → ', &amp; → &
        if not title or len(title) < 10:
            continue
        # Skip navigation/category links
        if "/story/" not in href:
            continue
        key = url_to_key(full_url)
        if key in seen:
            continue
        seen.add(key)

        results.append({
            "title": title,
            "url": full_url,
            "snippet": "",
        })

        if len(results) >= max_items:
            break

    return results


# ═══════════════════════════════════════════════════
#  RSS FETCH
# ═══════════════════════════════════════════════════

def fetch_rss(url, max_items=15):
    """
    Fetch RSS/Atom feed, return list of {title, url, snippet, pubDate}.
    Uses regex-based parsing to avoid external dependency.
    """
    results = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
        resp.raise_for_status()
        xml = resp.text
    except Exception as e:
        log(f"  ✗ RSS fetch failed {url}: {e}")
        return results

    # Parse RSS <item> entries
    items = re.findall(r"<item>(.*?)</item>", xml, re.DOTALL)
    if not items:
        # Try Atom <entry>
        items = re.findall(r"<entry>(.*?)</entry>", xml, re.DOTALL)

    for item_xml in items:
        # Title
        title_m = re.search(r"<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", item_xml, re.DOTALL)
        title = title_m.group(1).strip() if title_m else ""

        # Link
        link_m = re.search(r'<link[^>]*>(.*?)</link>', item_xml)
        if not link_m:
            link_m = re.search(r'<link[^>]*href="([^"]+)"', item_xml)
        link = link_m.group(1).strip() if link_m else ""

        # Snippet/description
        desc_m = re.search(r"<description>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</description>", item_xml, re.DOTALL)
        snippet = ""
        if desc_m:
            snippet = re.sub(r"<[^>]+>", " ", desc_m.group(1).strip())
            snippet = re.sub(r"\s+", " ", snippet).strip()[:500]

        # pubDate
        pub_m = re.search(r"<pubDate>(.*?)</pubDate>", item_xml)
        pub_date = pub_m.group(1).strip() if pub_m else ""

        if title and link:
            title = html_module.unescape(title)  # Fix HTML entities
            results.append({
                "title": title,
                "url": link,
                "snippet": snippet,
                "pubDate": pub_date,
            })

        if len(results) >= max_items:
            break

    return results


# ═══════════════════════════════════════════════════
#  FETCH ARTICLE CONTENT
# ═══════════════════════════════════════════════════

def fetch_content(url, timeout=12):
    """Fetch article page, extract readable text."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        resp.raise_for_status()
        text = resp.text
        # Remove script/style
        text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
        # Remove HTML tags
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        if len(text) > 8000:
            text = text[:8000]
        return text if len(text) > 100 else None
    except Exception as e:
        log(f"  ⚠ fetch_content failed: {e}")
        return None


# ═══════════════════════════════════════════════════
#  EXTRACT og:image
# ═══════════════════════════════════════════════════

def extract_og_image(url, timeout=10):
    """Extract og:image from article page."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        resp.raise_for_status()
        match = re.search(
            r'<meta\s+property="og:image"\s+content="([^"]+)"',
            resp.text, re.IGNORECASE
        )
        if match:
            img = match.group(1)
            try:
                ir = requests.head(img, headers=HEADERS, timeout=8)
                if ir.status_code == 200:
                    return img
            except:
                pass
        return None
    except Exception:
        return None


# ═══════════════════════════════════════════════════
#  GITHUB MODELS API (GPT-4o-mini, FREE)
# ═══════════════════════════════════════════════════

def call_llm(article_title, article_content, category_name):
    """Call GitHub Models for Chinese summary — dual-model fallback strategy.

    Strategy:
      1. Try GPT-4o-mini first (fast, free tier)
      2. If output is NOT Chinese → retry with Llama-3.1-70B (much better Chinese)
      3. If both fail → return a clear fallback message (NOT raw English)
    """
    # ── Token check ──
    if not GITHUB_TOKEN:
        log("⚠ GITHUB_TOKEN not set — using placeholder summary")
        return _fallback(article_title, article_content, "GITHUB_TOKEN 未配置")

    # ── Prompt (shared across models) ──
    prompt = textwrap.dedent(f"""\
你是一位宾州州立大学（Penn State University）新闻编辑，负责把英文新闻改写为中文日报摘要。

【任务】
阅读以下英文新闻内容，生成符合格式的中文摘要。

【新闻类别】{category_name}

【重要——必须遵守】
- TITLE_CN 和 SUMMARY 字段的正文部分必须全部使用中文书写，禁止出现英文。
- TITLE_EN 字段才允许使用英文。
- 如果你不确定某个术语的中文翻译，请使用中文描述替代。

【输出格式——严格按以下结构生成，不要多也不要少】
TITLE_CN: <精炼的中文标题，15-40字>
TITLE_EN: <英文原标题>
SUMMARY:
<strong>核心提炼：</strong><用2-4个自然段写中文摘要，250-500字。要求：
- 第一段概述核心事件
- 后续段落展开关键细节、数据、人物、背景
- 用<strong>标签加粗关键信息（人名、数据、机构名、成果名）
- 为中文读者提供必要的美国大学文化背景注解
- 不要用markdown格式，只输出纯HTML片段（p, strong, br标签）>

【英文新闻内容】
标题: {article_title}
正文: {article_content[:5000]}

请只输出上述格式的内容，不要有任何多余的解释。""")

    # ── Helpers ──
    def _call_api(model_name):
        """Single API call to GitHub Models."""
        resp = requests.post(
            GH_MODELS_URL,
            headers={
                "Authorization": f"Bearer {GITHUB_TOKEN}",
                "Content-Type": "application/json",
            },
            json={
                "model": model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 2048,
            },
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()

    def _is_chinese(text):
        """Rough check: Chinese characters ratio > 15% of (Chinese + Latin) chars."""
        if not text:
            return False
        cn = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        alpha = sum(1 for c in text if c.isalpha() and c.isascii())
        total = cn + alpha
        return total > 0 and cn / total > 0.15

    def _parse(raw):
        """Parse LLM output into structured fields."""
        title_cn = article_title
        title_en = article_title
        summary = article_content[:400]

        m_tcn = re.search(r"TITLE_CN:\s*(.+?)(?:\n|$)", raw)
        m_ten = re.search(r"TITLE_EN:\s*(.+?)(?:\n|$)", raw)
        m_sum = re.search(r"SUMMARY:\s*\n?(.*)", raw, re.DOTALL)

        if m_tcn:
            title_cn = m_tcn.group(1).strip()
        if m_ten:
            title_en = m_ten.group(1).strip()
        if m_sum:
            summary = m_sum.group(1).strip()

        title_cn = title_cn.replace('"', '\u201c').replace('"', '\u201d')

        if "核心提炼" not in summary:
            summary = "<strong>核心提炼：</strong>" + summary

        return {"title_cn": title_cn, "title_en": title_en, "summary": summary}

    # ── Step 1: Try GPT-4o-mini ──
    try:
        raw = _call_api("gpt-4o-mini")
        result = _parse(raw)

        if _is_chinese(result["summary"]) and _is_chinese(result["title_cn"]):
            log("  ✓ GPT-4o-mini → Chinese OK")
            return result

        # Not Chinese — try Llama
        log("  ⚠ GPT-4o-mini returned non-Chinese, switching to Llama-3.1-70B...")
    except Exception as e:
        status = getattr(e, 'response', None)
        if status is not None:
            log(f"  ✗ GPT-4o-mini API error HTTP {status.status_code}: {e}")
        else:
            log(f"  ✗ GPT-4o-mini API error: {e}")

    # ── Step 2: Fall back to Llama-3.1-70B (much stronger at Chinese) ──
    try:
        raw2 = _call_api("Meta-Llama-3.1-70B-Instruct")
        result2 = _parse(raw2)

        if _is_chinese(result2["summary"]):
            log("  ✓ Llama-3.1-70B → Chinese OK")
            return result2

        # Still not Chinese — return what we have with a warning
        log("  ✗ Llama-3.1-70B also returned non-Chinese")
        return _fallback(article_title, article_content, "AI 模型输出非中文")
    except Exception as e:
        status = getattr(e, 'response', None)
        if status is not None:
            log(f"  ✗ Llama-3.1-70B API error HTTP {status.status_code}")
        else:
            log(f"  ✗ Llama-3.1-70B API error: {e}")
        return _fallback(article_title, article_content, "API 调用失败")


def _fallback(article_title, article_content, reason):
    """Generate a clean fallback summary when LLM is unavailable."""
    snippet = article_content[:300].strip()
    return {
        "title_cn": article_title[:60],
        "title_en": article_title[:120],
        "summary": (
            f"<strong>核心提炼：</strong>"
            f"（{reason}，以下为原文片段供参考）<br><br>"
            f"{snippet}"
        )
    }

# ═══════════════════════════════════════════════════
#  SOURCE DETECTION
# ═══════════════════════════════════════════════════

def detect_source(url, default_meta):
    """Detect source label/class from URL, fall back to category default."""
    if "onwardstate.com" in url:
        return "Onward State", "onward"
    elif "nittanysportsnow.com" in url:
        return "Nittany Sports Now", ""
    elif "si.com" in url:
        return "Sports Illustrated", ""
    elif "collegian.psu.edu" in url:
        return "Daily Collegian", "collegian"
    elif "gopsusports.com" in url:
        return "Penn State Athletics", "psu"
    elif "psu.edu" in url:
        return "Penn State News", "psu"
    return default_meta["source"], default_meta["source_class"]


# ═══════════════════════════════════════════════════
#  MAIN: PROCESS ALL CATEGORIES
# ═══════════════════════════════════════════════════

def process_all_categories():
    history_data, known_urls, edition_num = load_history()
    edition_str = str(edition_num)
    log(f"Edition #{edition_str} | {TODAY_CN} {WEEKDAY} | {len(known_urls)} known URLs")
    log(f"GitHub Models: {'✓ configured' if GITHUB_TOKEN else '✗ MISSING (dry-run)'}")

    cards = []

    # ── Step 0: pre-fetch RSS for sports & supplemental ──
    log("\n📡 Fetching RSS feeds...")
    sports_articles = []
    for feed_url in SPORTS_RSS_FEEDS:
        items = fetch_rss(feed_url)
        log(f"  {feed_url.split('/')[2]}: {len(items)} articles")
        sports_articles.extend(items)

    onward_articles = fetch_rss(ONWARD_RSS)
    log(f"  onwardstate.com: {len(onward_articles)} articles")

    # Build a pool: all scraped + RSS articles, indexed by keyword
    all_pool = []

    for cat_name in CATEGORY_ORDER:
        meta = CATEGORY_META[cat_name]

        log(f"\n{'─'*50}")
        log(f"🔍 [{cat_name}]")

        candidates = []

        if cat_name == "体育动态":
            # Use sports RSS
            for a in sports_articles:
                candidates.append({
                    "title": a["title"],
                    "url": a["url"],
                    "snippet": a.get("snippet", ""),
                    "source_label": "Nittany Sports Now" if "nittany" in a["url"] else "Onward State",
                })

        elif cat_name in CATEGORY_SCRAPE:
            # Scrape psu.edu category pages
            for scrape_url in CATEGORY_SCRAPE[cat_name]:
                items = scrape_psu_category(scrape_url)
                log(f"  scrape {scrape_url.split('/news/')[1]}: {len(items)} articles")
                for item in items:
                    candidates.append({
                        "title": item["title"],
                        "url": item["url"],
                        "snippet": item.get("snippet", ""),
                        "source_label": "Penn State News",
                    })

        # Fallback: for 演出预告/校友活动, also check Onward State
        if len(candidates) < 3 and cat_name in ("演出预告", "校友活动"):
            log(f"  ⚠ few psu.edu results, adding Onward State candidates...")
            for a in onward_articles:
                candidates.append({
                    "title": a["title"],
                    "url": a["url"],
                    "snippet": a.get("snippet", ""),
                    "source_label": "Onward State",
                })

        if not candidates:
            log(f"  ✗ No candidates for [{cat_name}]")
            continue

        log(f"  Total candidates: {len(candidates)}")

        # ── Pick first non-duplicate ──
        chosen = None
        for c in candidates:
            if not is_dup(c["url"], known_urls):
                chosen = c
                break

        if not chosen:
            log(f"  ⚠ All candidates are duplicates, using first anyway")
            chosen = candidates[0]

        log(f"  ✓ Selected: {chosen['title'][:80]}")
        log(f"    URL: {chosen['url'][:80]}")

        # ── Fetch full content ──
        content = fetch_content(chosen["url"])
        if not content:
            content = chosen.get("snippet", chosen["title"])
            log(f"  Using snippet as content ({len(content)} chars)")

        # ── LLM summary ──
        log(f"  🤖 Calling GitHub Models (GPT-4o-mini)...")
        ds = call_llm(chosen["title"], content, cat_name)

        # ── og:image ──
        image_url = extract_og_image(chosen["url"])
        if image_url:
            log(f"  🖼 og:image: {image_url[:70]}...")

        # ── Source detection ──
        src_label, src_class = detect_source(chosen["url"], meta)

        # ── Build card ──
        card = {
            "id": meta["id"],
            "category_cn": cat_name,
            "tag_class": meta["tag"],
            "title_cn": ds["title_cn"],
            "title_en": ds["title_en"],
            "image": image_url or "",
            "summary": ds["summary"],
            "source": src_label,
            "source_class": src_class,
            "date_cn": TODAY_CN,
            "url": chosen["url"],
            "cat_id": meta["cat_id"],
        }
        cards.append(card)

        # Mark URL as used for this run
        known_urls.add(chosen["url"])

    return cards, edition_str, history_data


# ═══════════════════════════════════════════════════
#  HTML BUILDING
# ═══════════════════════════════════════════════════

def build_card_html(card):
    source_class = card.get("source_class", "")
    if source_class:
        source_span = f'<span class="{source_class} source-badge">{card["source"]}</span>'
    else:
        source_span = f'<span class="source-badge">{card["source"]}</span>'

    if card.get("image"):
        img_block = f'<div class="card-image"><img style="opacity:1" src="{card["image"]}" alt="" loading="lazy"></div>'
    else:
        img_block = ""

    return f'''        <!-- {card["category_cn"]} -->
    <article class="news-card" id="{card["id"]}">
      <span class="card-tag {card["tag_class"]}">{card["category_cn"]}</span>
      <div class="card-body">
        <h2 class="card-title">{card["title_cn"]}</h2>
        <div class="card-title-en">{card["title_en"]}</div>
        {img_block}
        <p class="card-summary">
{card["summary"]}
        </p>
        <div class="card-meta">
          <div class="meta-left">
            {source_span}
          </div>
          <div class="meta-right">
            <span class="card-date">{card["date_cn"]}</span>
          </div>
        </div>
        <a class="card-link" href="{card["url"]}" target="_blank" rel="noopener">阅读原文<span class="arrow">→</span></a>
      </div>
    </article>'''


def build_lead_cn(cards):
    keywords = []
    for c in cards:
        t = c["title_cn"]
        t = t.replace("：", "·").replace("——", "·")
        parts = t.split("·")
        kw = parts[0].strip()[:18]
        keywords.append(kw)
    return " • ".join(keywords)


def build_lead_en(cards):
    keywords = []
    for c in cards:
        t = c["title_en"]
        t = t.split(":")[0].split("·")[0].strip()[:30]
        keywords.append(t)
    return " · ".join(keywords)


def update_html_files(cards, edition_str):
    all_cards_html = "\n\n".join(build_card_html(c) for c in cards)
    lead_cn = build_lead_cn(cards)
    lead_en = build_lead_en(cards)

    # ── Read template from current index.html ──
    index_path = os.path.join(BASE, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        template = f.read()

    # ── 1. Daily page: psu-news-{TODAY}.html ──
    daily = template
    daily = re.sub(
        r'<title>宾州州立大学 Six A Day \| \d{4}年\d{1,2}月\d{1,2}日</title>',
        f'<title>宾州州立大学 Six A Day | {TODAY_CN}</title>', daily
    )
    daily = re.sub(
        r'(id="todayDate">)\d{4}年\d{1,2}月\d{1,2}日 星期.',
        f'\\1{TODAY_CN} {WEEKDAY}', daily
    )
    daily = re.sub(r'第\s*\d+\s*期', f'第{edition_str}期', daily)
    daily = re.sub(
        r'<div class="lead-cn">.*?</div>',
        f'<div class="lead-cn">{lead_cn}</div>', daily, flags=re.DOTALL
    )
    daily = re.sub(
        r'<div class="lead-en">.*?</div>',
        f'<div class="lead-en">Today\'s Focus · {lead_en}</div>', daily, flags=re.DOTALL
    )

    # Replace news grid
    grid_start = daily.find('<div class="news-grid">')
    section_div = daily.find('\n\n  <div class="section-divider"', grid_start)
    if section_div != -1:
        # Find the closing </div> before section-divider (that's the news-grid close)
        before = daily[:section_div]
        last_close = before.rfind('</div>')
        if last_close != -1:
            daily = daily[:grid_start] + '<div class="news-grid">\n\n' + all_cards_html + '\n\n  </div>' + daily[last_close:]

    daily_path = os.path.join(BASE, f"psu-news-{TODAY}.html")
    with open(daily_path, "w", encoding="utf-8") as f:
        f.write(daily)
    log(f"[OK] psu-news-{TODAY}.html")

    # ── 2. index.html ──
    index_html = template
    index_html = re.sub(
        r'<title>宾州州立大学 Six A Day \| \d{4}年\d{1,2}月\d{1,2}日</title>',
        f'<title>宾州州立大学 Six A Day | {TODAY_CN}</title>', index_html
    )
    index_html = re.sub(
        r'(id="todayDate">)\d{4}年\d{1,2}月\d{1,2}日 星期.',
        f'\\1{TODAY_CN} {WEEKDAY}', index_html
    )
    index_html = re.sub(r'第\s*\d+\s*期', f'第{edition_str}期', index_html)
    index_html = re.sub(
        r'<div class="lead-cn">.*?</div>',
        f'<div class="lead-cn">{lead_cn}</div>', index_html, flags=re.DOTALL
    )
    index_html = re.sub(
        r'<div class="lead-en">.*?</div>',
        f'<div class="lead-en">Today\'s Focus · {lead_en}</div>', index_html, flags=re.DOTALL
    )

    grid_start = index_html.find('<div class="news-grid">')
    section_div = index_html.find('\n\n  <div class="section-divider"', grid_start)
    if section_div != -1:
        before = index_html[:section_div]
        last_close = before.rfind('</div>')
        if last_close != -1:
            index_html = index_html[:grid_start] + '<div class="news-grid">\n\n' + all_cards_html + '\n\n  </div>' + index_html[last_close:]

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_html)
    log(f"[OK] index.html")

    # ── 3. archive.html ──
    archive_path = os.path.join(BASE, "archive.html")
    with open(archive_path, "r", encoding="utf-8") as f:
        archive = f.read()

    archive = re.sub(r'共\s*\d+\s*期', f'共 {edition_str} 期', archive)

    archive_card = f'''      <!-- 第{edition_str}期 — {TODAY_CN} - AUTO -->
      <div class="edition-card">
        <div class="edition-date">{TODAY_CN} · 第{edition_str}期</div>
        <div class="edition-keywords">{lead_cn}</div>
        <div class="edition-links">
          <a href="psu-news-{TODAY}.html" class="btn-edition">查看本期</a>
          <a href="index.html" class="btn-edition secondary">返回最新 →</a>
        </div>
      </div>
'''
    marker = "<!-- AUTO-APPEND-MARKER - DO NOT REMOVE -->"
    archive = archive.replace(marker, archive_card + "\n" + marker)

    with open(archive_path, "w", encoding="utf-8") as f:
        f.write(archive)
    log(f"[OK] archive.html")

    # ── 4. archive-catalog.html ──
    cat_path = os.path.join(BASE, "archive-catalog.html")
    with open(cat_path, "r", encoding="utf-8") as f:
        catalog = f.read()

    for card in cards:
        cat_id = card["cat_id"]
        section_start = catalog.find(f'<div class="cat-section" id="{cat_id}">')
        if section_start == -1:
            log(f"  ⚠ Section {cat_id} not found")
            continue

        next_section = catalog.find('<div class="cat-section"', section_start + 1)
        if next_section == -1:
            next_section = len(catalog)
        section = catalog[section_start:next_section]

        count_match = re.search(r'(<span class="count">)(\d+)(</span>)', section)
        if count_match:
            old_count = int(count_match.group(2))
            new_count = old_count + 1
            pos = section_start + count_match.start()
            catalog = (
                catalog[:pos]
                + f'{count_match.group(1)}{new_count}{count_match.group(3)}'
                + catalog[pos + len(count_match.group(0)):]
            )

        news_list_start = catalog.find('<div class="news-list">', section_start)
        if news_list_start != -1:
            insert_pos = news_list_start + len('<div class="news-list">\n')
            news_item = (
                f'              <a class="news-item" href="psu-news-{TODAY}.html#{card["id"]}">'
                f'<span class="ni-cat">{card["category_cn"]}</span>'
                f'<span class="ni-title">{card["title_cn"]}</span>'
                f'<span class="ni-date">{TODAY_CN}</span></a>\n'
            )
            catalog = catalog[:insert_pos] + news_item + catalog[insert_pos:]

    with open(cat_path, "w", encoding="utf-8") as f:
        f.write(catalog)
    log(f"[OK] archive-catalog.html")

    # ── 5. history.json ──
    hist_path = os.path.join(BASE, "history.json")
    with open(hist_path, "r", encoding="utf-8") as f:
        history = json.load(f)

    for card in cards:
        entry = {
            "url": card["url"],
            "title_cn": card["title_cn"],
            "category": card["category_cn"],
            "source": card["source"],
            "date": TODAY,
        }
        if card.get("image"):
            entry["image_url"] = card["image"]
        history["shown_news_history"].append(entry)

    history["last_updated"] = TODAY

    with open(hist_path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    log(f"[OK] history.json ({len(history['shown_news_history'])} total)")

    # Verify
    with open(hist_path, "r", encoding="utf-8") as f:
        json.load(f)
    log(f"[OK] history.json valid JSON")


# ═══════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════

def main():
    log("=" * 60)
    log("PSU Daily News Auto-Builder (v2 — Scrape + GitHub Models)")
    log(f"Date: {TODAY_CN} {WEEKDAY}")

    # ── Token diagnostic: test if GITHUB_TOKEN can actually call GitHub Models ──
    if GITHUB_TOKEN:
        token_preview = GITHUB_TOKEN[:8] + "..." if len(GITHUB_TOKEN) > 8 else GITHUB_TOKEN
        log(f"GitHub Models token: {token_preview} (len={len(GITHUB_TOKEN)})")
        try:
            test_resp = requests.post(
                GH_MODELS_URL,
                headers={
                    "Authorization": f"Bearer {GITHUB_TOKEN}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": "Say OK"}],
                    "max_tokens": 5,
                },
                timeout=30,
            )
            if test_resp.status_code == 200:
                log("✓ GitHub Models API reachable — token OK")
            else:
                body = test_resp.text[:200]
                log(f"✗ GitHub Models API returned HTTP {test_resp.status_code}: {body}")
        except Exception as e:
            log(f"✗ GitHub Models API unreachable: {e}")
    else:
        log("✗ GITHUB_TOKEN MISSING — LLM summaries disabled")
    log("=" * 60)

    cards, edition_str, history_data = process_all_categories()

    if len(cards) == 0:
        log("\n✗✗✗ NO CARDS FOUND — aborting ✗✗✗")
        sys.exit(1)

    log(f"\n{'='*60}")
    log(f"✓ {len(cards)}/6 cards ready")
    for i, c in enumerate(cards):
        img_status = "🖼" if c.get("image") else "✗"
        log(f"  #{i+1} [{c['category_cn']}] {c['title_cn'][:60]}... {img_status}")

    log(f"\n📄 Building HTML files...")
    update_html_files(cards, edition_str)

    keywords = [c["title_cn"].split("：")[0].split("·")[0][:20] for c in cards]
    log(f"\n{'='*60}")
    log(f"✅ BUILD COMPLETE — Edition #{edition_str} | {TODAY_CN}")
    log(f"   {' • '.join(keywords)}")
    log(f"   Files: index.html, psu-news-{TODAY}.html, archive.html, archive-catalog.html, history.json")
    log(f"{'='*60}")


if __name__ == "__main__":
    main()
