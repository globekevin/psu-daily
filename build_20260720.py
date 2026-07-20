#!/usr/bin/env python3
"""Build PSU Daily News for 2026-07-20 — Edition #25"""

import json, re, shutil, datetime

# ── 6 News Cards Data ──────────────────────────────────────────────
cards = [
    {
        "id": "news-1",
        "category_cn": "传媒学院",
        "tag_class": "tag-comm",
        "title_cn": "Bellisario 学院应届毕业生 Greg Finberg 跻身 Hearst 新闻竞赛全国决赛——作品聚焦校园枪击受害者家属",
        "title_en": "Recent journalism graduate among competitors for national championship: Greg Finberg advances to Hearst Awards national finals · Penn State News",
        "image": "https://psu-gatsby-files-prod.s3.amazonaws.com/s3fs-public/styles/16_9_1000w/public/2026/06/gregfinberg-hearst_0.jpg?h=fa3a8807&itok=EUQUIIcA",
        "summary": (
            "<strong>核心提炼：</strong>"
            "Bellisario 传播学院<strong> 2026 年应届毕业生 Greg Finberg</strong>被选入<strong> Hearst 新闻奖</strong>（被誉为「大学新闻界的普利策」）<strong>全国锦标赛决赛</strong>，"
            "成为 29 名决赛选手之一、<strong>PSU 唯一代表</strong>。"
            "Finberg 的参赛作品聚焦<strong>校园枪击案受害者家属</strong>的深层报道，"
            "展现了他对突发性社会创伤的<strong>敏锐洞察与叙事能力</strong>。"
            "Hearst 竞赛涵盖写作、摄影、音频、电视、多媒体五大领域，"
            "每年吸引全美 100+ 所高校新闻学院参赛。"
            "Bellisario 学院近年来在 Hearst 奖项中屡有斩获，"
            "Finberg 此次晋级延续了学院在<strong>深度新闻报道与人物特写</strong>方向的传统优势。"
            "决赛将于<strong> 6 月初在旧金山</strong>举行，"
            "最终排名将计入 PSU 在 Hearst 综合排名中的年度积分。"
        ),
        "source": "Penn State News",
        "source_class": "psu",
        "date_cn": "2026年6月1日",
        "url": "https://www.psu.edu/news/bellisario-college-communications/story/recent-journalism-graduate-among-competitors-national",
        "history_category": "传媒学院"
    },
    {
        "id": "news-2",
        "category_cn": "演出预告",
        "tag_class": "tag-up",
        "title_cn": "PSU Berkey Creamery 8 月 1 日起全面无现金化：只接受信用卡、借记卡与移动支付，现金与支票退出历史",
        "title_en": "Penn State Berkey Creamery to go cashless Aug. 1: mobile pay, credit/debit cards only; cash and checks no longer accepted · Penn State News",
        "image": "https://psu-gatsby-files-prod.s3.amazonaws.com/s3fs-public/styles/16_9_1000w/public/2022/03/150813_Creamery_Misc-1_1.jpg?h=a1e1a043&itok=rW6nff6w",
        "summary": (
            "<strong>核心提炼：</strong>"
            "Penn State 地标性机构 <strong>Berkey Creamery</strong>宣布<strong> 2026 年 8 月 1 日起全面实现无现金运营</strong>，"
            "所有门店自此<strong>不再接受现金与支票</strong>，仅接受 <strong>Visa、MasterCard、Discover、American Express</strong> "
            "以及 <strong>Apple Pay、Google Pay、Samsung Pay</strong> 等移动支付方式。"
            "Creamery 管理层表示，无现金化将<strong>提升结账效率、减少排队等待时间</strong>，"
            "并<strong>降低现金管理成本与安全风险</strong>。"
            "此前 Creamery 已逐步引导顾客向电子支付过渡，"
            "8 月 1 日的正式切换是这一进程的最终阶段。"
            "对于<strong>仅持有现金的游客</strong>，Creamery 将在门店内设置<strong>自助现金转卡终端（reverse ATM）</strong>，"
            "可将现金兑换为预付借记卡（不收取手续费），确保所有顾客皆可获得 Creamery 经典冰淇淋。"
            "Berkey Creamery 自 1865 年创办以来日均生产<strong>约 4,500 磅冰淇淋</strong>，是 State College 最具代表性的校园地标之一。"
        ),
        "source": "Penn State News",
        "source_class": "psu",
        "date_cn": "2026年7月15日",
        "url": "https://www.psu.edu/news/agricultural-sciences/story/penn-state-berkey-creamery-go-cashless-aug-1",
        "history_category": "演出预告"
    },
    {
        "id": "news-3",
        "category_cn": "校友活动",
        "tag_class": "tag-alumni",
        "title_cn": "Penn State 2026「Roar Tour」校友巡游开放报名：校长 Bendapudi 将亲赴全美多城与校友面对面交流",
        "title_en": "Penn Staters invited to sign up for 2026 Roar Tour: President Bendapudi to visit alumni chapters across the US · Penn State News",
        "image": "https://psu-gatsby-files-prod.s3.amazonaws.com/s3fs-public/styles/16_9_1000w/public/2026/07/roar-tour_penn-state-news-2000x1500-copy.jpg?h=10229ec2&itok=FcNMo7VS",
        "summary": (
            "<strong>核心提炼：</strong>"
            "Penn State 校友会正式启动<strong> 2026 年「Roar Tour」校友巡游</strong>报名，"
            "<strong>校长 Neeli Bendapudi</strong> 将亲自率团前往全美多个城市，"
            "与各地校友分会成员<strong>面对面交流</strong>大学最新发展动态与未来战略。"
            "Roar Tour 是 Penn State 校友会的<strong>年度旗舰活动</strong>，"
            "2026 年巡游站点覆盖<strong>东西海岸及中西部主要城市</strong>，"
            "每站安排校长演讲、校友社交酒会、校园吉祥物互动等环节。"
            "Bendapudi 自 2022 年上任以来持续强化<strong>校友-母校纽带</strong>，"
            "此次巡游将重点分享<strong> 2026-2030 战略规划进展</strong>，"
            "包括学术卓越、学生可负担性、研究创新三大支柱。"
            "所有 Penn State 校友均可<strong>免费报名</strong>参加所在城市的站点活动，"
            "具体日程与城市列表见校友会官网。"
        ),
        "source": "Penn State News",
        "source_class": "psu",
        "date_cn": "2026年7月17日",
        "url": "https://www.psu.edu/news/alumni-association/story/penn-staters-invited-sign-2026-roar-tour",
        "history_category": "校友活动"
    },
    {
        "id": "news-4",
        "category_cn": "体育动态",
        "tag_class": "tag-sports",
        "title_cn": "两名 2026 届防守新秀正式加入 PSU 橄榄球大名单：DE Hurst 与 LB Murphy 将为 Nittany Lions 防线注入新鲜血液",
        "title_en": "Two key defensive 2026 prospects join football roster: DE Jordan Hurst and LB Marcus Murphy bolster Nittany Lions' defensive depth · Nittany Lions Wire",
        "image": "https://nittanylionswire.usatoday.com/gcdn/authoring/authoring-images/2026/07/16/SPSU/90940745007-usatsi-26847331.jpg?crop=4040,2273,x0,y363&width=3200&height=1801&format=pjpg&auto=webp",
        "summary": (
            "<strong>核心提炼：</strong>"
            "Penn State 橄榄球队在<strong> 2026 赛季前</strong>迎来两名高潜力防守新秀："
            "<strong>防守端锋 Jordan Hurst</strong>（DE）和<strong>线卫 Marcus Murphy</strong>（LB），"
            "二人已正式加入球队大名单，将参与<strong>夏季训练营</strong>备战 9 月 5 日对阵 Marshall 的赛季揭幕战。"
            "Hurst 身高 6 尺 4 寸、体重 250 磅，以<strong>爆发力与冲传技巧</strong>著称，"
            "在高中最后一季交出<strong> 12 次擒杀</strong>的亮眼成绩单。"
            "Murphy 则是全面型线卫，兼具<strong>防跑直觉与覆盖能力</strong>，"
            "被教练组视为可即插即用的<strong>轮换力量</strong>。"
            "防守协调员 <strong>Tom Allen</strong> 在春季训练中强调需要补充<strong>前线深度</strong>，"
            "这两名新秀的到来将有效缓解防守组在<strong>高强度 Big Ten 赛程</strong>中的轮换压力。"
            "PSU 防守组上赛季排名 Big Ten <strong>前五</strong>，新赛季目标冲击<strong>大学橄榄球季后赛</strong>。"
        ),
        "source": "Nittany Lions Wire",
        "source_class": "",
        "date_cn": "2026年7月16日",
        "url": "https://nittanylionswire.usatoday.com/story/sports/college/nittany-lions/football/2026/07/16/two-key-defensive-2026-prospects-join-football-roster/90940636007/",
        "history_category": "体育动态"
    },
    {
        "id": "news-5",
        "category_cn": "行政人事",
        "tag_class": "tag-admin",
        "title_cn": "校董会批准 2027-28 住餐费率：UP 综合涨幅 2.5% 为九年来最低，白楼研究生公寓连续第七年不涨价",
        "title_en": "Board of Trustees approves housing and dining rates for 2027-28: aggregate UP increase lowest in 9 years; White Course Apartments frozen 7th straight year · Penn State News",
        "image": "https://psu-gatsby-files-prod.s3.amazonaws.com/s3fs-public/styles/16_9_1000w/public/IMG_4618.jpeg?h=71976bb4&itok=2SEhLSNa",
        "summary": (
            "<strong>核心提炼：</strong>"
            "Penn State 校董会<strong> 7 月 17 日</strong>正式批准 2027-28 学年住餐费率方案，"
            "关键数据：<strong>University Park 综合涨幅仅 2.5%</strong>——为<strong> 2018-19 学年以来最低</strong>，"
            "PSU 住餐成本继续<strong>低于 Big Ten 联盟平均水平</strong>。"
            "具体而言：UP 翻新双人间每学期涨 <strong>$119</strong> 至 <strong>$4,885</strong>；"
            "Signature Dining Plan 涨 <strong>$75</strong> 至 <strong>$3,063</strong>；"
            "二者合计每学期 <strong>$7,948</strong>。"
            "<strong>白楼研究生公寓（White Course Apartments）连续第七年不涨价</strong>，一卧一卫无家具公寓维持 $1,168/月。"
            "Commonwealth Campuses 方面：Abington 等七校区住餐合并涨 <strong>1.5%</strong>（+$110/学期至 $7,439）；"
            "Greater Allegheny 等三校区住宿费<strong>连续第二年冻结</strong>。"
            "财务副总裁 <strong>Sara Thorndike</strong> 称「目标是将学生及家庭成本增幅压到最低，同时持续投资安全舒适的校园居住空间」。"
            "HFS 同时公布资本更新计划：2027-28 将启动 <strong>Pollock 区第三阶段翻新</strong>"
            "（Hiester/Shulze 重开，Porter/Shunk 停用），"
            "全联邦校区设施更新预算 <strong>$2,000 万</strong>。"
            "此外 <strong>LiveOn 学生成功补助金</strong>进入第六年，预计 2027-28 向 447 名学生发放 <strong>$130 万+</strong>。"
        ),
        "source": "Penn State News",
        "source_class": "psu",
        "date_cn": "2026年7月17日",
        "url": "https://www.psu.edu/news/administration/story/board-trustees-approves-housing-and-dining-rates-2027-28-academic-year",
        "history_category": "行政人事"
    },
    {
        "id": "news-6",
        "category_cn": "科研成果",
        "tag_class": "tag-research",
        "title_cn": "能源价格冲击：短期拖慢州经济，长期倒逼能效提升——PSU 农学院揭示能源危机中的「创造性破坏」效应",
        "title_en": "Energy price shocks slow state economies, spur energy efficiency: Penn State research finds short-term pain leads to long-term efficiency gains · Penn State News",
        "image": "https://psu-gatsby-files-prod.s3.amazonaws.com/s3fs-public/styles/16_9_1000w/public/2026/07/adobestock_1957530938_web.jpeg?h=53aeb022&itok=ytNRGgNp",
        "summary": (
            "<strong>核心提炼：</strong>"
            "Penn State <strong>农业科学学院</strong>研究团队发表最新成果："
            "利用<strong>美国 50 个州 1970-2020 年间</strong>的面板数据，"
            "系统分析能源价格冲击对各州经济的<strong>短期与长期影响</strong>。"
            "核心发现：(1) <strong>短期负面</strong>——能源价格每上涨 10%，"
            "州 GDP 增长率在随后一年平均下降 <strong>0.15-0.3 个百分点</strong>，"
            "制造业与运输业首当其冲；(2) <strong>长期正面</strong>——冲击后 3-5 年内，"
            "受冲击州的<strong>能源效率投资显著上升</strong>（设备升级、建筑节能改造、新能源替代），"
            "这种「创造性破坏」效应部分甚至<strong>完全抵消</strong>了初始经济损失；"
            "(3) <strong>政策放大效应</strong>——拥有<strong>可再生能源组合标准（RPS）</strong>"
            "和<strong>能效资源标准（EERS）</strong>的州，在冲击后能效提升速度<strong>显著更快</strong>，"
            "经济恢复也更快。研究指出，当前<strong>全球能源价格波动加剧</strong>的背景下，"
            "各州应主动建立<strong>能效政策缓冲机制</strong>，将短期冲击转化为长期竞争力。"
            "该研究对<strong>气候政策与能源安全交叉领域</strong>具有重要政策启示。"
        ),
        "source": "Penn State News",
        "source_class": "psu",
        "date_cn": "2026年7月17日",
        "url": "https://www.psu.edu/news/agricultural-sciences/story/energy-price-shocks-slow-state-economies-spur-energy-efficiency",
        "history_category": "科研成果"
    },
]

TODAY = "2026-07-20"
TODAY_CN = "2026年7月20日"
WEEKDAY = "星期一"
EDITION_NUM = "25"
BASE = "/Users/mac/WorkBuddy/2026-06-25-12-43-57/psu-news-daily"

# ── 1. Update history.json ─────────────────────────────────────────
with open(f"{BASE}/history.json", "r", encoding="utf-8") as f:
    history = json.load(f)

for card in cards:
    entry = {
        "url": card["url"],
        "title_cn": card["title_cn"],
        "category": card["history_category"],
        "source": card["source"],
        "date": TODAY,
    }
    if card.get("image"):
        entry["image_url"] = card["image"]
    history["shown_news_history"].append(entry)
history["last_updated"] = TODAY

with open(f"{BASE}/history.json", "w", encoding="utf-8") as f:
    json.dump(history, f, ensure_ascii=False, indent=2)
print("[OK] history.json updated")

# Verify JSON
with open(f"{BASE}/history.json", "r", encoding="utf-8") as f:
    json.load(f)
print("[OK] history.json valid JSON")

# ── 2. Build HTML card snippets ────────────────────────────────────
def build_card_html(card):
    source_class = card.get("source_class", "")
    if source_class:
        source_span = f'<span class="{source_class} source-badge">{card["source"]}</span>'
    else:
        source_span = f'<span class="source-badge">{card["source"]}</span>'

    return f'''        <!-- {cards.index(card)+1}. {card["category_cn"]} -->
    <article class="news-card" id="{card["id"]}">
      <span class="card-tag {card["tag_class"]}">{card["category_cn"]}</span>
      <div class="card-body">
        <h2 class="card-title">{card["title_cn"]}</h2>
        <div class="card-title-en">{card["title_en"]}</div>
        <div class="card-image"><img src="{card["image"]}" alt="" loading="lazy" onerror="this.parentElement.style.display='none'"></div>
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

all_cards_html = "\n\n".join(build_card_html(c) for c in cards)

# ── 3. Build daily page: psu-news-YYYY-MM-DD.html ──────────────────
# Copy from previous day (7/19) which has the stable template
with open(f"{BASE}/psu-news-2026-07-19.html", "r", encoding="utf-8") as f:
    daily = f.read()

# Update title
daily = daily.replace(
    "<title>宾州州立大学 Six A Day | 2026年7月19日</title>",
    f"<title>宾州州立大学 Six A Day | {TODAY_CN}</title>"
)

# Update date display (todayDate span)
daily = re.sub(
    r'(<div class="date">)\d{4}年\d{1,2}月\d{1,2}日 星期.',
    f'\\1{TODAY_CN} {WEEKDAY}',
    daily
)

# Update edition numbers (handle both "第 23 期" and "第23期" formats)
daily = re.sub(r'第\s*\d+\s*期', f'第 {EDITION_NUM} 期', daily)

# Update lead-cn
daily_lead_cn = "Hearst新闻竞赛决赛 • Creamery八月无现金化 • Roar Tour校友巡游 • 两名防守新秀加盟橄榄球 • 住餐费率九年来最低 • 能源冲击与「创造性破坏」"
daily = re.sub(
    r'<div class="lead-cn">.*?</div>',
    f'<div class="lead-cn">{daily_lead_cn}</div>',
    daily,
    flags=re.DOTALL
)

# Update lead-en
daily_lead_en = "Today's Focus · Hearst Journalism Finals · Creamery Goes Cashless · Roar Tour 2026 · Defensive Prospects · Housing Rates · Energy Shocks & Efficiency"
daily = re.sub(
    r'<div class="lead-en">.*?</div>',
    f'<div class="lead-en">{daily_lead_en}</div>',
    daily,
    flags=re.DOTALL
)

# Replace the entire news grid
grid_start = daily.find('<div class="news-grid">')
# Find the closing </div> that ends the news-grid, right before the section divider
grid_end_marker = '</div>\n\n  <div class="section-divider"'
grid_end = daily.find(grid_end_marker, grid_start)
if grid_end == -1:
    grid_end_marker = '</div>\n\n        <p class="card-summary">'
    grid_end = daily.find(grid_end_marker, grid_start)
if grid_end == -1:
    grid_end = daily.find('\n</main>', grid_start)

if grid_start != -1 and grid_end != -1:
    daily = daily[:grid_start] + '<div class="news-grid">\n\n' + all_cards_html + '\n\n  </div>' + daily[grid_end:]

with open(f"{BASE}/psu-news-{TODAY}.html", "w", encoding="utf-8") as f:
    f.write(daily)
print(f"[OK] psu-news-{TODAY}.html created")

# ── 4. Update index.html ──────────────────────────────────────────
with open(f"{BASE}/index.html", "r", encoding="utf-8") as f:
    index = f.read()

# Update title
index = re.sub(
    r'<title>宾州州立大学 Six A Day \| \d{4}年\d{1,2}月\d{1,2}日</title>',
    f'<title>宾州州立大学 Six A Day | {TODAY_CN}</title>',
    index
)
# Update date display
index = re.sub(
    r'(<div class="date">)\d{4}年\d{1,2}月\d{1,2}日 星期.',
    f'\\1{TODAY_CN} {WEEKDAY}',
    index
)
# Update lead-cn
index = re.sub(
    r'<div class="lead-cn">.*?</div>',
    f'<div class="lead-cn">{daily_lead_cn}</div>',
    index,
    flags=re.DOTALL
)
# Update lead-en
index = re.sub(
    r'<div class="lead-en">.*?</div>',
    f'<div class="lead-en">{daily_lead_en}</div>',
    index,
    flags=re.DOTALL
)
# Update edition
index = re.sub(r'第\s*\d+\s*期', f'第 {EDITION_NUM} 期', index)

# Replace news grid
grid_start = index.find('<div class="news-grid">')
grid_end_marker = '</div>\n\n  <div class="section-divider"'
grid_end = index.find(grid_end_marker, grid_start)
if grid_start != -1 and grid_end != -1:
    index = index[:grid_start] + '<div class="news-grid">\n\n' + all_cards_html + '\n\n  </div>' + index[grid_end:]

with open(f"{BASE}/index.html", "w", encoding="utf-8") as f:
    f.write(index)
print("[OK] index.html updated")

# ── 5. Update archive.html ────────────────────────────────────────
with open(f"{BASE}/archive.html", "r", encoding="utf-8") as f:
    archive = f.read()

# Update count header
archive = re.sub(r'共 \d+ 期', f'共 {EDITION_NUM} 期', archive)

# Build archive card
archive_card = f'''      <!-- 第{EDITION_NUM}期 — {TODAY_CN} - AUTO -->
      <div class="edition-card">
        <div class="edition-date">{TODAY_CN} · 第{EDITION_NUM}期</div>
        <div class="edition-keywords">{daily_lead_cn}</div>
        <div class="edition-links">
          <a href="psu-news-{TODAY}.html" class="btn-edition">查看本期</a>
          <a href="index.html" class="btn-edition secondary">返回最新 →</a>
        </div>
      </div>
'''

# Insert before AUTO-APPEND-MARKER
marker = "<!-- AUTO-APPEND-MARKER - DO NOT REMOVE -->"
archive = archive.replace(marker, archive_card + "\n" + marker)

with open(f"{BASE}/archive.html", "w", encoding="utf-8") as f:
    f.write(archive)
print("[OK] archive.html updated")

# ── 6. Update archive-catalog.html ────────────────────────────────
with open(f"{BASE}/archive-catalog.html", "r", encoding="utf-8") as f:
    catalog = f.read()

category_map = {
    "传媒学院": "cat-comm",
    "演出预告": "cat-events",
    "校友活动": "cat-alumni",
    "体育动态": "cat-sports",
    "行政人事": "cat-admin",
    "科研成果": "cat-research",
}

for card in cards:
    cat = card["history_category"]
    cat_id = category_map[cat]

    # Update count for this category
    count_pattern = re.compile(
        rf'(<span class="cat-count">)(\d+)(</span>)'
    )
    section_start = catalog.find(f'<div class="cat-section" id="{cat_id}">')
    if section_start == -1:
        print(f"[WARN] Category section not found: {cat_id}")
        continue
    
    # Find next section or end
    next_section = catalog.find('<div class="cat-section"', section_start + 1)
    section = catalog[section_start:next_section] if next_section != -1 else catalog[section_start:]
    
    match = count_pattern.search(section)
    if match:
        old_count = int(match.group(2))
        abs_pos = section_start + match.start()
        new_span = f'{match.group(1)}{old_count + 1}{match.group(3)}'
        catalog = catalog[:abs_pos] + new_span + catalog[abs_pos + len(match.group(0)):]

    # Prepend news-item entry
    news_list_pos = catalog.find('<div class="news-list">', section_start)
    if news_list_pos != -1:
        insert_pos = news_list_pos + len('<div class="news-list">\n')
        news_item = f'              <a class="news-item" href="psu-news-{TODAY}.html#{card["id"]}"><span class="ni-cat">{cat}</span><span class="ni-title">{card["title_cn"]}</span><span class="ni-date">{TODAY_CN}</span></a>\n'
        catalog = catalog[:insert_pos] + news_item + catalog[insert_pos:]

with open(f"{BASE}/archive-catalog.html", "w", encoding="utf-8") as f:
    f.write(catalog)
print("[OK] archive-catalog.html updated")

print(f"\n{'='*60}")
print(f"Build complete for {TODAY_CN} — Edition #{EDITION_NUM}")
print(f"{'='*60}")
for i, c in enumerate(cards, 1):
    has_img = "✓" if c.get("image") else "✗"
    print(f"  #{i} [{c['category_cn']}] {c['title_cn'][:55]}... | img={has_img}")
