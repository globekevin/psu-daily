#!/usr/bin/env python3
"""
PSU Daily News Engine — 纯数据层
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
抓取 psu.edu + RSS → DeepSeek 中文摘要 → 返回结构化 JSON。
不含任何 HTML 生成逻辑，专供 API 服务调用。

Required env: DEEPSEEK_API_KEY
"""

import os, sys, json, re, datetime, textwrap
import html as html_module
from datetime import date, timedelta
from pathlib import Path
import requests

# ═══════════════════════════════════════════════════
#  CONFIGURATION
# ═══════════════════════════════════════════════════

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"

DEDUP_WINDOW = 14
MAX_CARDS = 6

# US Eastern time
ET = datetime.timezone(datetime.timedelta(hours=-4))

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

CATEGORY_SCRAPE = {
    "传媒学院": ["https://www.psu.edu/news/bellisario-college-communications/"],
    "演出预告": [
        "https://www.psu.edu/news/arts-and-architecture/",
        "https://www.psu.edu/news/arts-and-entertainment/",
    ],
    "校友活动": ["https://www.psu.edu/news/development-and-alumni-relations/"],
    "行政人事": ["https://www.psu.edu/news/administration/"],
    "科研成果": [
        "https://www.psu.edu/news/research/",
        "https://www.psu.edu/news/engineering/",
        "https://www.psu.edu/news/agricultural-sciences/",
    ],
}

SPORTS_RSS_FEEDS = [
    "https://nittanysportsnow.com/feed/",
    "https://onwardstate.com/feed/",
]

CATEGORY_META = {
    "传媒学院": {"id": "news-1", "tag": "tag-comm",     "source": "Penn State News",    "source_class": "psu"},
    "演出预告": {"id": "news-2", "tag": "tag-up",       "source": "Penn State News",    "source_class": "psu"},
    "校友活动": {"id": "news-3", "tag": "tag-alumni",   "source": "Penn State News",    "source_class": "psu"},
    "体育动态": {"id": "news-4", "tag": "tag-sports",   "source": "Nittany Sports Now", "source_class": ""},
    "行政人事": {"id": "news-5", "tag": "tag-admin",    "source": "Penn State News",    "source_class": "psu"},
    "科研成果": {"id": "news-6", "tag": "tag-research", "source": "Penn State News",    "source_class": "psu"},
}

CATEGORY_ORDER = ["传媒学院", "演出预告", "校友活动", "体育动态", "行政人事", "科研成果"]

# ═══════════════════════════════════════════════════
#  DATA PATHS
# ═══════════════════════════════════════════════════

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
HISTORY_FILE = DATA_DIR / "history.json"


def log(msg):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


# ═══════════════════════════════════════════════════
#  HISTORY
# ═══════════════════════════════════════════════════

def init_history():
    """Create history.json if it doesn't exist."""
    if not HISTORY_FILE.exists():
        data = {"shown_news_history": [], "last_updated": ""}
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return data
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_history():
    """Load history, return recent URLs (DEDUP_WINDOW days) for dedup."""
    data = init_history()
    cutoff = date.today() - timedelta(days=DEDUP_WINDOW)
    recent_urls = set()
    dates_seen = set()
    for e in data.get("shown_news_history", []):
        if e.get("date"):
            dates_seen.add(e["date"])
            try:
                d = date.fromisoformat(e["date"])
                if d >= cutoff:
                    recent_urls.add(e.get("url", ""))
            except Exception:
                pass
    edition = len(dates_seen) + 1
    return data, recent_urls, edition


def save_history(history_data):
    """Persist history to disk."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history_data, f, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════
#  UTILITY
# ═══════════════════════════════════════════════════

def url_to_key(url):
    url = url.strip().rstrip("/")
    url = re.sub(r"^https?://(www\.)?", "", url)
    return url


# ═══════════════════════════════════════════════════
#  SCRAPE: psu.edu
# ═══════════════════════════════════════════════════

def scrape_psu_category(url, max_items=12):
    results = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
        resp.raise_for_status()
        page_html = resp.text
    except Exception as e:
        log(f"  ✗ scrape failed {url}: {e}")
        return results

    links = re.findall(
        r'<a\s[^>]*href="(/news/(?:[^/]+/)?story/[^"]+)"[^>]*>([^<]+)</a>',
        page_html
    )
    seen = set()
    for href, title in links:
        full_url = "https://www.psu.edu" + href
        title = html_module.unescape(title.strip())
        if not title or len(title) < 10:
            continue
        if "/story/" not in href:
            continue
        key = url_to_key(full_url)
        if key in seen:
            continue
        seen.add(key)
        results.append({"title": title, "url": full_url, "snippet": ""})
        if len(results) >= max_items:
            break
    return results


# ═══════════════════════════════════════════════════
#  RSS FETCH
# ═══════════════════════════════════════════════════

def fetch_rss(url, max_items=15):
    results = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
        resp.raise_for_status()
        xml = resp.text
    except Exception as e:
        log(f"  ✗ RSS fetch failed {url}: {e}")
        return results

    items = re.findall(r"<item>(.*?)</item>", xml, re.DOTALL)
    if not items:
        items = re.findall(r"<entry>(.*?)</entry>", xml, re.DOTALL)

    for item_xml in items:
        title_m = re.search(r"<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", item_xml, re.DOTALL)
        title = title_m.group(1).strip() if title_m else ""

        link_m = re.search(r'<link[^>]*>(.*?)</link>', item_xml)
        if not link_m:
            link_m = re.search(r'<link[^>]*href="([^"]+)"', item_xml)
        link = link_m.group(1).strip() if link_m else ""

        desc_m = re.search(r"<description>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</description>", item_xml, re.DOTALL)
        snippet = ""
        if desc_m:
            snippet = re.sub(r"<[^>]+>", " ", desc_m.group(1).strip())
            snippet = re.sub(r"\s+", " ", snippet).strip()[:500]

        pub_m = re.search(r"<pubDate>(.*?)</pubDate>", item_xml)
        pub_date = pub_m.group(1).strip() if pub_m else ""

        if title and link:
            title = html_module.unescape(title)
            results.append({
                "title": title, "url": link, "snippet": snippet, "pubDate": pub_date,
            })
        if len(results) >= max_items:
            break
    return results


# ═══════════════════════════════════════════════════
#  FETCH ARTICLE CONTENT
# ═══════════════════════════════════════════════════

def fetch_content(url, timeout=12):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        resp.raise_for_status()
        text = resp.text
        text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        if len(text) > 8000:
            text = text[:8000]
        return text if len(text) > 100 else None
    except Exception as e:
        log(f"  ⚠ fetch_content failed: {e}")
        return None


# ═══════════════════════════════════════════════════
#  og:image
# ═══════════════════════════════════════════════════

def extract_og_image(url, timeout=10):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        resp.raise_for_status()
        match = re.search(
            r'<meta\s+property="og:image"\s+content="([^"]+)"',
            resp.text, re.IGNORECASE
        )
        if match:
            return match.group(1)
        return None
    except Exception:
        return None


# ═══════════════════════════════════════════════════
#  DEEPSEEK API
# ═══════════════════════════════════════════════════

def call_llm(article_title, article_content, category_name):
    if not DEEPSEEK_API_KEY:
        return _fallback(article_title, article_content, "DEEPSEEK_API_KEY 未配置")

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
TITLE_CN: <中文新闻标题，10-18字。凝练、有新闻意境>
TITLE_EN: <英文原标题>
SUMMARY:
<strong>核心提炼：</strong><一段中文新闻导语。要求：
- 全文连标点在内严格控制在120-140字之间，不得超过140字
- 开门见山，交代5W1H
- 用<strong>标签加粗2-3处关键信息
- 只用纯HTML片段（p, strong, br标签）

【英文新闻内容】
标题: {article_title}
正文: {article_content[:5000]}

请只输出上述格式的内容，不要有任何多余的解释。""")

    def _is_chinese(text):
        if not text:
            return False
        cn = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        alpha = sum(1 for c in text if c.isalpha() and c.isascii())
        total = cn + alpha
        return total > 0 and cn / total > 0.15

    def _parse(raw):
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

        body_match = re.match(r'^(<strong>核心提炼：</strong>)(.*)$', summary, re.DOTALL)
        if body_match:
            prefix, body = body_match.group(1), body_match.group(2).strip()
            if len(body) > 140:
                log(f"  ⚠ Summary too long ({len(body)} chars), trimming to 140")
                truncated = body[:140]
                for punct in ['。', '；', '，']:
                    last = truncated.rfind(punct)
                    if last > 80:
                        truncated = truncated[:last + 1]
                        break
                summary = prefix + truncated

        return {"title_cn": title_cn, "title_en": title_en, "summary": summary}

    try:
        resp = requests.post(
            DEEPSEEK_URL,
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": DEEPSEEK_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 2048,
            },
            timeout=120,
        )
        resp.raise_for_status()
        raw = resp.json()["choices"][0]["message"]["content"].strip()
        result = _parse(raw)
        if _is_chinese(result["summary"]) and _is_chinese(result["title_cn"]):
            log("  ✓ DeepSeek → Chinese OK")
            return result
        log("  ⚠ DeepSeek returned non-Chinese output")
        return _fallback(article_title, article_content, "AI 模型输出非中文")
    except Exception as e:
        status = getattr(e, 'response', None)
        if status is not None:
            log(f"  ✗ DeepSeek API error HTTP {status.status_code}: {e}")
        else:
            log(f"  ✗ DeepSeek API error: {e}")
        return _fallback(article_title, article_content, f"API 调用失败 ({str(e)[:80]})")


def _fallback(article_title, article_content, reason):
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
#  MAIN: PROCESS ALL CATEGORIES → CARDS
# ═══════════════════════════════════════════════════

def generate_news(target_date_str=None):
    """Run the full pipeline and return cards + metadata.

    Returns: dict {
        "date": "2026-07-31",
        "date_cn": "2026年7月31日",
        "weekday": "星期五",
        "edition": 42,
        "cards": [ ... ]
    }
    """
    if target_date_str:
        now_dt = date.fromisoformat(target_date_str)
    else:
        now_dt = date.today()
    
    now_et = datetime.datetime.now(ET)
    today_str = now_dt.isoformat()
    today_cn = f"{now_dt.year}年{now_dt.month}月{now_dt.day}日"
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday = weekdays[now_dt.weekday()]

    history_data, known_urls, edition_num = load_history()
    edition_str = str(edition_num)
    log(f"Edition #{edition_str} | {today_cn} {weekday} | {len(known_urls)} recent URLs")
    log(f"DeepSeek API: {'✓ configured' if DEEPSEEK_API_KEY else '✗ MISSING'}")

    # ── Step 0: pre-fetch RSS ──
    log("\n📡 Fetching RSS feeds...")
    sports_articles = []
    for feed_url in SPORTS_RSS_FEEDS:
        items = fetch_rss(feed_url)
        log(f"  {feed_url.split('/')[2]}: {len(items)} articles")
        sports_articles.extend(items)
    onward_articles = [a for a in sports_articles if "onwardstate.com" in a.get("url", "")]

    cards = []
    cat_candidates = {}

    for cat_name in CATEGORY_ORDER:
        meta = CATEGORY_META[cat_name]
        log(f"\n{'─'*50}")
        log(f"🔍 [{cat_name}]")

        candidates = []

        if cat_name == "体育动态":
            for a in sports_articles:
                candidates.append({
                    "title": a["title"],
                    "url": a["url"],
                    "snippet": a.get("snippet", ""),
                    "source_label": "Nittany Sports Now" if "nittany" in a["url"] else "Onward State",
                })
        elif cat_name in CATEGORY_SCRAPE:
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

        # Fallback: Onward State for 演出预告/校友活动
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
        cat_candidates[cat_name] = list(candidates)

        # Pick first non-duplicate
        chosen = None
        for c in candidates:
            if c["url"] not in known_urls:
                chosen = c
                break

        if not chosen:
            log(f"  ⚠ All candidates are duplicates, skipping [{cat_name}]")
            continue

        log(f"  ✓ Selected: {chosen['title'][:80]}")

        content = fetch_content(chosen["url"])
        if not content:
            content = chosen.get("snippet", chosen["title"])

        log(f"  🤖 Calling DeepSeek API...")
        ds = call_llm(chosen["title"], content, cat_name)

        image_url = extract_og_image(chosen["url"])
        if image_url:
            log(f"  🖼 og:image: {image_url[:70]}...")

        src_label, src_class = detect_source(chosen["url"], meta)

        card = {
            "id": "",
            "category_cn": cat_name,
            "tag_class": meta["tag"],
            "title_cn": ds["title_cn"],
            "title_en": ds["title_en"],
            "image": image_url or "",
            "summary": ds["summary"],
            "source": src_label,
            "source_class": src_class,
            "date_cn": today_cn,
            "url": chosen["url"],
        }
        cards.append(card)
        known_urls.add(chosen["url"])

    # ── Fill-up ──
    while len(cards) < MAX_CARDS:
        added = False
        for cat_name in CATEGORY_ORDER:
            if len(cards) >= MAX_CARDS:
                break
            meta = CATEGORY_META[cat_name]
            reserved = cat_candidates.get(cat_name, [])
            chosen = None
            for c in reserved:
                if c["url"] not in known_urls:
                    chosen = c
                    break
            if not chosen:
                continue

            log(f"\n{'─'*50}")
            log(f"🔄 Fill-up from [{cat_name}]: {chosen['title'][:80]}")

            content = fetch_content(chosen["url"])
            if not content:
                content = chosen.get("snippet", chosen["title"])

            ds = call_llm(chosen["title"], content, cat_name)
            image_url = extract_og_image(chosen["url"])
            src_label, src_class = detect_source(chosen["url"], meta)

            card = {
                "id": "",
                "category_cn": cat_name,
                "tag_class": meta["tag"],
                "title_cn": ds["title_cn"],
                "title_en": ds["title_en"],
                "image": image_url or "",
                "summary": ds["summary"],
                "source": src_label,
                "source_class": src_class,
                "date_cn": today_cn,
                "url": chosen["url"],
            }
            cards.append(card)
            known_urls.add(chosen["url"])
            added = True

        if not added:
            log(f"\n⚠ Fill-up exhausted, stopping at {len(cards)} cards")
            break

    # Re-assign sequential IDs
    for i, card in enumerate(cards):
        card["id"] = f"news-{i+1}"

    # ── Save to history ──
    for card in cards:
        entry = {
            "url": card["url"],
            "title_cn": card["title_cn"],
            "category": card["category_cn"],
            "source": card["source"],
            "date": today_str,
        }
        if card.get("image"):
            entry["image_url"] = card["image"]
        history_data["shown_news_history"].append(entry)

    history_data["last_updated"] = today_str
    save_history(history_data)

    result = {
        "date": today_str,
        "date_cn": today_cn,
        "weekday": weekday,
        "edition": edition_num,
        "cards": cards,
    }

    # ── Also save daily JSON snapshot ──
    daily_file = DATA_DIR / f"{today_str}.json"
    with open(daily_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    log(f"\n[OK] Saved to {daily_file}")

    return result


def load_daily(date_str=None):
    """Load news for a specific date. If None, load today's or latest available."""
    if date_str:
        daily_file = DATA_DIR / f"{date_str}.json"
    else:
        daily_file = DATA_DIR / f"{date.today().isoformat()}.json"

    if daily_file.exists():
        with open(daily_file, "r", encoding="utf-8") as f:
            return json.load(f)

    # Fallback: find the latest available
    if not date_str:
        files = sorted(DATA_DIR.glob("20*.json"), reverse=True)
        if files:
            with open(files[0], "r", encoding="utf-8") as f:
                return json.load(f)
    return None


# ═══════════════════════════════════════════════════
#  ENTRY POINT (for cron)
# ═══════════════════════════════════════════════════

if __name__ == "__main__":
    log("=" * 60)
    log("PSU Daily News Engine")
    result = generate_news()
    log(f"\n{'='*60}")
    log(f"✅ DONE — {len(result['cards'])} cards, Edition #{result['edition']}")
    log(f"   {' • '.join(c['title_cn'][:30] for c in result['cards'])}")
    log(f"{'='*60}")
