#!/usr/bin/env python3
"""Build PSU Daily News for 2026-07-19 — Edition #24"""

import json, re, shutil, datetime

# ── 6 News Cards Data ──────────────────────────────────────────────
cards = [
    {
        "id": "news-1",
        "category_cn": "传媒学院",
        "tag_class": "tag-comm",
        "title_cn": "Bellisario 学院 Sundar 教授团队发现：AI 对医生诊断「第二意见」——同意则增信、反对则引发不信任",
        "title_en": "AI disagreement may shake patient trust in doctors: Bellisario College research shows when AI agrees with doctor, patient credibility rises; disagreement increases perceived laziness · Penn State News",
        "image": "https://psu-gatsby-files-prod.s3.amazonaws.com/s3fs-public/styles/16_9_1000w/public/2026/07/gettyimages-2274592130.jpg?h=119335f7&itok=-WSq7MdF",
        "summary": (
            "<strong>核心提炼：</strong>"
            "Bellisario 学院 <strong>Evan Pugh 大学教授 S. Shyam Sundar</strong>（James P. Jimirro 媒体效果讲席教授）团队"
            "在《<strong>International Journal of Human-Computer Studies</strong>》发表研究："
            "团队让 135 名成年人接受 AI 模拟医生「Dr. Alex」的在线心理健康咨询（认知行为疗法 CBT），"
            "然后提供 AI 助手 <strong>CareBot 的「第二意见」</strong>——"
            "当 AI 同意医生建议时，<strong>患者认为诊断更可信</strong>；"
            "当 AI 反对时，患者对<strong>「医学不确定性」和「医生懒惰度」</strong>的感知显著上升。"
            "该效应仅在患者认为医生<strong>「更像真人」</strong>时出现"
            "（超过一半参与者认为 AI 模拟的医生很人性化）。"
            "对<strong>机器偏见（machine heuristic）更强</strong>的人群——认为 AI 比人更准确客观的人——AI 反对的负面影响尤其强烈，"
            "说明 AI 在患者心中拥有<strong>「播下怀疑种子」的惊人权威</strong>。"
            "一作 <strong>Cheng「Chris」Chen</strong>（Oregon State 助理教授，PSU 博士毕业）建议医生"
            "可用<strong>隐晦方式</strong>传达 AI 分歧（如「我用的某个工具标记了几个值得深挖的点，我们一起看看」）。"
            "研究对远程医疗、在线问诊等场域有重要启示。"
        ),
        "source": "Penn State News",
        "source_class": "psu",
        "date_cn": "2026年7月16日",
        "url": "https://www.psu.edu/news/research/story/ai-disagreement-may-shake-patient-trust-doctors",
        "history_category": "传媒学院"
    },
    {
        "id": "news-2",
        "category_cn": "演出预告",
        "tag_class": "tag-up",
        "title_cn": "PSU 学生农场夏季植物义卖 7/23-24：番茄、黄瓜、生菜、香草应有尽有，现摘现卖现金结算",
        "title_en": "Student Farm and Food Systems to host annual Summer Plant Sale, July 23-24: garden seedlings, houseplants and late-season crops for the community · Penn State News",
        "image": "https://psu-gatsby-files-prod.s3.amazonaws.com/s3fs-public/styles/16_9_1000w/public/2026/04/_dsc1634.jpg?h=4521fff0&itok=KZ2B_kSe",
        "summary": (
            "<strong>核心提炼：</strong>"
            "Penn State <strong>学生农场与食品系统（Student Farm and Food Systems）</strong>"
            "将于<strong> 7 月 23 日（周四）和 24 日（周五）</strong>每天 <strong>10:30-13:00</strong>"
            "在 <strong>Tyson 温室 Headhouse III</strong>（Curtin 路旁，East Parking Deck 可停车）"
            "举办<strong>年度夏季植物义卖</strong>，面向全校师生与公众开放。"
            "温室经理 <strong>Zoe Seitz</strong> 介绍本次品种包括<strong>西葫芦、黄瓜、南瓜、结球生菜、甘蓝、香草</strong>等晚夏作物——"
            "这些苗已精心培育以适应宾州中部条件，<strong>可持续采收至 10-11 月</strong>。"
            "此外还有<strong>多肉植物与其他室内盆栽</strong>出售。"
            "价格：<strong>每株 $2.50 或 15 株 $30</strong>（多年生植物与多肉价格另标）。"
            "注意：<strong>仅接受现金或支票</strong>，请自带纸箱/袋装苗。"
            "该活动凸显<strong>秋延后种植（late-season planting）</strong>的可持续园艺理念——"
            "生菜、甘蓝等作物在凉爽秋季反而更茁壮。"
        ),
        "source": "Penn State News",
        "source_class": "psu",
        "date_cn": "2026年7月16日",
        "url": "https://www.psu.edu/news/student-affairs/story/student-farm-and-food-systems-host-annual-summer-plant-sale-july-23-24",
        "history_category": "演出预告"
    },
    {
        "id": "news-3",
        "category_cn": "校友活动",
        "tag_class": "tag-alumni",
        "title_cn": "Charlene Friedman 里程碑捐赠创建「Friedman PEACE 计划」：推动同理心与共情科研从实验室走向社区实践",
        "title_en": "Landmark gift from longtime Penn State volunteer Charlene Friedman to build PEACE Program promoting empathy and compassion — renamed Friedman PEACE Program · Penn State News",
        "image": "https://psu-gatsby-files-prod.s3.amazonaws.com/s3fs-public/styles/16_9_1000w/public/2026/07/friedman-image-2.jpg?h=04ed459f&itok=yHNT2d1U",
        "summary": (
            "<strong>核心提炼：</strong>"
            "长期 Penn State 志愿者与本地商界领袖 <strong>Charlene Friedman</strong>"
            "（Seton Hall 教育学士，Industrial-Commercial Realty LLC 持有者）"
            "做出<strong>里程碑级捐赠</strong>，推动 <strong>PEACE 计划（同理心、觉察与共情教育项目）</strong>大幅升级——"
            "该计划更名为 <strong>「Friedman PEACE 计划」</strong>，"
            "核心使命为<strong>推进正念、同理心与共情研究</strong>，并加速成果转化为社区实践。"
            "PEACE 计划由 <strong>Mark T. Greenberg</strong> 在 1998 年创建的 Edna Bennett Pierce 预防研究中心孵化——"
            "Friedman 与 Pierce 为多年好友，"
            "她表示「Edna 的慷慨激励我播下一颗种子，去培育一个更友善、更有思考力的世界」。"
            "中心主任 <strong>Max Crowley</strong> 表示，"
            "Friedman 的捐赠将扩大该计划的<strong>研究组合</strong>、"
            "促进 <strong>Centre County 本地教师/咨询师/社工/医疗人员网络</strong>建设，"
            "让科学发现<strong>立即转化为政策变革与社区影响</strong>。"
            "现有已启动项目包括：<strong>K-12 学校正念教师培训</strong>（Sebrina Doyle Fosco）；"
            "<strong>联合国教科文组织青年共情建设</strong>（Mark Brennan）；"
            "<strong>产前压力对婴儿健康的影响研究</strong>（Heidemarie Laurent）。"
            "校长 <strong>Neeli Bendapudi</strong> 称「这份礼物将助跨学科卓越与社会传播相结合，产生持久影响」。"
        ),
        "source": "Penn State News",
        "source_class": "psu",
        "date_cn": "2026年7月13日",
        "url": "https://www.psu.edu/news/development-and-alumni-relations/story/landmark-gift-build-program-promoting-empathy-and-compassion",
        "history_category": "校友活动"
    },
    {
        "id": "news-4",
        "category_cn": "体育动态",
        "tag_class": "tag-sports",
        "title_cn": "Phil Steele 季前分析：PSU 跑卫组 Big Ten 第 5、全国第 16 ——三头马车 Hansen/Peoples/Martin 各司其职，进攻组整体「可期但缺精英」",
        "title_en": "How Penn State's offense grades out in the Big Ten and national rankings: Phil Steele ranks RBs No. 5 in Big Ten, QBs 33rd nationally · Sports Illustrated",
        "image": "https://images2.minutemediacdn.com/image/upload/c_crop,x_0,y_36,w_4421,h_2486/c_fill,w_1440,ar_1440:810,f_auto,q_auto,g_auto/images/ImagnImages/mmsport/all_penn_state/01kvqzzvp2aq041tgdjg.jpg",
        "summary": (
            "<strong>核心提炼：</strong>"
            "Sports Illustrated 援引 <strong>Phil Steele 2026 大学橄榄球年鉴</strong>深度分析 Penn State 进攻组各位置排名："
            "最高评级为<strong>跑卫组（RB）</strong>——Big Ten <strong>第 5</strong>、全国 <strong>第 16</strong>，"
            "归功于教练 <strong>Matt Campbell</strong> 构建的<strong>三跑卫轮换体系</strong>："
            "前 Iowa State 主力 <strong>Carson Hansen</strong>（稳定推进）、"
            "Ohio State 转学生 <strong>James Peoples</strong>（big-play 威胁）、"
            "Pinstripe Bowl 亮眼回归的 <strong>Quinton Martin Jr.</strong>（兼具两者特质），"
            "外加恢复健康的 <strong>Cam Wallace</strong>。"
            "<strong>四分卫组排名 Big Ten 第 9、全国第 33</strong>——看似偏低，"
            "实际反映 <strong>Rocco Becht</strong> 虽是 FBS 经验最丰富的 QB，"
            "但在 <strong>精英层级</strong>仍不及 OSU/Oregon/Indiana 等队。"
            "<strong>接球组整体偏弱</strong>，缺乏顶级天赋。"
            "进攻协调员 <strong>Taylor Mouser</strong> 春季在甄别核心 playmaker，"
            "但真正答案要等 <strong>9 月 5 日对阵 Marshall</strong> 才能揭晓。"
        ),
        "source": "Sports Illustrated",
        "source_class": "",
        "date_cn": "2026年7月17日",
        "url": "https://www.si.com/college/pennstate/football/how-penn-state-offense-grades-out-in-the-big-ten-and-national-rankings",
        "history_category": "体育动态"
    },
    {
        "id": "news-5",
        "category_cn": "行政人事",
        "tag_class": "tag-admin",
        "title_cn": "校董会通过 2027-28 预算与学费方案：Commonwealth Campuses 宾州本科生学费连续第 5 年冻结，UP 涨 2.5%",
        "title_en": "Board of Trustees approves 2027-28 budget and tuition plan: 5th consecutive tuition freeze for in-state Commonwealth Campus undergrads, 2.5% UP increase, 3% merit raise pool · Penn State News",
        "image": "https://psu-gatsby-files-prod.s3.amazonaws.com/s3fs-public/styles/16_9_1000w/public/2026/06/2026-psu-universitypark-1884.jpg?h=13e6b738&itok=f2trShuv",
        "summary": (
            "<strong>核心提炼：</strong>"
            "Penn State 校董会<strong> 7 月 17 日在 Pennsylvania College of Technology</strong>投票通过 2027-28 学年预算与学费方案，"
            "关键数据：<strong>Commonwealth Campuses 宾州本科学费连续第 5 年冻结</strong>；"
            "University Park 宾州本科学费上涨 <strong>2.5%</strong>（低于当前通胀率）；"
            "外州本科生 UP 涨 <strong>4%</strong>、Commonwealth 涨 <strong>1%</strong>；"
            "全校预算<strong>约 111 亿美元</strong>，其中教育与通用（E&G）预算<strong> 29 亿美元连续第三年实现平衡</strong>。"
            "为平衡 E&G，各学院/校区/行政部门<strong>合计削减 2460 万美元</strong>（-1.1%）。"
            "新支出包括：<strong>3% 绩效加薪池 4900 万美元</strong>、"
            "<strong>研究生助理津贴涨 4%</strong>、"
            "<strong>员工福利成本增 2300 万美元</strong>（主要由医保驱动）、"
            "<strong>教职晋升 600 万美元</strong>。"
            "校长 <strong>Neeli Bendapudi</strong> 称「每份预算都需深思熟虑的优先排序——该方案在限制学费增长的同时进行战略投资」。"
            "财务副总裁 <strong>Sara Thorndike</strong> 指出<strong>住餐费涨幅为 UP 九年来最低</strong>。"
            "该预算<strong> 2027 年 7 月 1 日生效</strong>。"
        ),
        "source": "Penn State News",
        "source_class": "psu",
        "date_cn": "2026年7月17日",
        "url": "https://www.psu.edu/news/administration/story/board-trustees-approves-2027-28-budget-and-tuition-plan",
        "history_category": "行政人事"
    },
    {
        "id": "news-6",
        "category_cn": "科研成果",
        "tag_class": "tag-research",
        "title_cn": "《Corrosion Science》：PSU 团队发现金属原子排列可形成「腐蚀高速公路」——为先进核反应堆材料设计提供原子级指南",
        "title_en": "Metals' atomic arrangement can create 'corrosion highways' in nuclear reactors: Penn State simulations reveal long-range ordering accelerates molten salt corrosion · Penn State News / Corrosion Science",
        "image": "https://psu-gatsby-files-prod.s3.amazonaws.com/s3fs-public/styles/16_9_1000w/public/2026/07/lro-resized.jpg?h=84071268&itok=t16aMQ69",
        "summary": (
            "<strong>核心提炼：</strong>"
            "Penn State <strong>工程科学与力学系</strong>团队在《<strong>Corrosion Science</strong>》发表突破性研究："
            "利用 Penn State <strong>ROAR 超级计算机</strong>进行<strong>原子级模拟</strong>"
            "（每次模拟 1 纳秒需计算约 1 天），"
            "揭示<strong>镍铬合金（nichrome）</strong>在<strong>熔盐（先进核反应堆冷却剂）</strong>中的腐蚀机制——"
            "关键发现：(1) 当镍铬合金中原子呈<strong>长程有序（long-range ordering）</strong>排列时，"
            "会形成贯穿材料内部的<strong>「渗透腐蚀高速公路」</strong>，"
            "腐蚀速度远超短程有序或无规排列；(2) 暴露仅 <strong>3 纳秒</strong>（三十亿分之一秒），"
            "长程有序表面即变得<strong>粗糙多坑</strong>，而短程有序与随机排列保持光滑。"
            "通讯作者 <strong>Reika Katsumata</strong> 与一作 <strong>Hamza Arkoub</strong> 称，"
            "基于此理解团队正在构建<strong>高尺度预测模型</strong>实时模拟合金腐蚀演化——"
            "此前因缺乏原子级腐蚀机理认知而受限。"
            "研究由 NSF 与 DOE 资助，联合 <strong>Idaho National Laboratory</strong>。"
        ),
        "source": "Penn State News",
        "source_class": "psu",
        "date_cn": "2026年7月13日",
        "url": "https://www.psu.edu/news/research/story/metals-atomic-arrangement-can-create-corrosion-highways-nuclear-reactors",
        "history_category": "科研成果"
    },
]

TODAY = "2026-07-19"
TODAY_CN = "2026年7月19日"
WEEKDAY = "星期日"
EDITION_NUM = "24"
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
        source_span = f'<span class="psu source-badge">{card["source"]}</span>'
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
with open(f"{BASE}/psu-news-2026-07-18.html", "r", encoding="utf-8") as f:
    daily = f.read()

# Replace date/edition
daily = daily.replace("2026年7月18日", TODAY_CN)
daily = daily.replace("星期" + ("五" if "18" in "18" else ""), f"星期{WEEKDAY[-1]}")  # HACK: quick fix below
daily = re.sub(r'星期\S', f'星期{WEEKDAY[-1]}', daily, count=1)  # Actually let's fix properly
daily = daily.replace("第23期", f"第{EDITION_NUM}期")

# Wait, the edition number appears in the date context. Let me be more careful.
# The original has "第23期" 
daily = daily.replace("<title>宾州州立大学 Six A Day | 2026年7月18日</title>", f"<title>宾州州立大学 Six A Day | {TODAY_CN}</title>")

# Fix weekday in todayDate
daily = re.sub(
    r'(id="todayDate">)\d{4}年\d{1,2}月\d{1,2}日 星期.',
    f'\\1{TODAY_CN} {WEEKDAY}',
    daily
)

# Fix edition number 
daily = re.sub(r'第\d+期', f'第{EDITION_NUM}期', daily)

# Replace lead-cn
daily_lead_cn = "AI第二意见撼动医生信任 • 夏季植物义卖本周 • Friedman里程碑捐赠 • PSU进攻组季前排名 • 校董会通过2027-28预算 • 核反应堆「腐蚀高速公路」"
daily = re.sub(
    r'<div class="lead-cn">.*?</div>',
    f'<div class="lead-cn">{daily_lead_cn}</div>',
    daily,
    flags=re.DOTALL
)

# Replace the entire news grid
# Find the news grid start and end
grid_start = daily.find('<div class="news-grid">')
grid_end = daily.find('</div>\n\n  <div class="section-divider"', grid_start)
if grid_end == -1:
    # Try alternative end marker
    grid_end = daily.find('</div>\n\n        <p class="card-summary">', grid_start)
    if grid_end == -1:
        # Just find the next major section
        grid_end = daily.find('\n</main>', grid_start)

if grid_start != -1:
    daily = daily[:grid_start] + '<div class="news-grid">\n\n' + all_cards_html + '\n\n  </div>' + daily[grid_end:]

# Fix any remaining 7/18 references in card-date spans
daily = daily.replace('2026年7月18日', TODAY_CN)

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
    r'(id="todayDate">)\d{4}年\d{1,2}月\d{1,2}日 星期.',
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
# Update edition
index = re.sub(r'第\d+期', f'第{EDITION_NUM}期', index)

# Replace news grid
grid_start = index.find('<div class="news-grid">')
grid_end = index.find('</div>\n\n  <div class="section-divider"', grid_start)
if grid_start != -1 and grid_end != -1:
    index = index[:grid_start] + '<div class="news-grid">\n\n' + all_cards_html + '\n\n  </div>' + index[grid_end:]

with open(f"{BASE}/index.html", "w", encoding="utf-8") as f:
    f.write(index)
print("[OK] index.html updated")

# ── 5. Update archive.html ────────────────────────────────────────
with open(f"{BASE}/archive.html", "r", encoding="utf-8") as f:
    archive = f.read()

# Update count header (e.g. "共 23 期" → "共 24 期")
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

# For each category, prepend a news-item entry and increment the count
category_map = {
    "传媒学院": ("cat-comm", "传媒学院"),
    "演出预告": ("cat-events", "演出预告"),
    "校友活动": ("cat-alumni", "校友活动"),
    "体育动态": ("cat-sports", "体育动态"),
    "行政人事": ("cat-admin", "行政人事"),
    "科研成果": ("cat-research", "科研成果"),
}

for card in cards:
    cat = card["history_category"]
    cat_id = category_map[cat][0]

    # Update count: find the count span for this category
    count_pattern = re.compile(
        rf'(<span class="cat-count">)(\d+)(</span>)',
        re.DOTALL
    )
    # Find the right section
    section_start = catalog.find(f'<div class="cat-section" id="{cat_id}">')
    if section_start == -1:
        continue
    section_end = catalog.find('</div>\n    </div>', section_start)
    if section_end == -1:
        section_end = catalog.find('<div class="cat-section"', section_start + 1)
    
    section = catalog[section_start:section_end]
    match = count_pattern.search(section)
    if match:
        old_count = int(match.group(2))
        new_span = f'{match.group(1)}{old_count + 1}{match.group(3)}'
        catalog = catalog[:section_start + match.start()] + new_span + catalog[section_start + match.end():]

    # Prepend news-item entry
    news_list_start = catalog.find('<div class="news-list">', section_start)
    if news_list_start != -1:
        insert_pos = news_list_start + len('<div class="news-list">\n')
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
    print(f"  #{i} [{c['category_cn']}] {c['title_cn'][:50]}... | img={has_img}")
