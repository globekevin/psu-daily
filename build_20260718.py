#!/usr/bin/env python3
"""Build PSU Daily News for 2026-07-18 — 第 23 期"""
import json, shutil, os, re

ROOT = "/Users/mac/WorkBuddy/2026-06-25-12-43-57/psu-news-daily"
TODAY = "2026-07-18"
YESTERDAY = "2026-07-17"
TODAY_FILE = f"psu-news-{TODAY}.html"
YESTERDAY_FILE = f"psu-news-{YESTERDAY}.html"
EDITION = "23"
WEEKDAY = "星期六"
THEME_CN = "Bellisario纪录片克罗地亚首映 · Ag Progress Days农业AI展 · 校友年度捐赠6.63亿创纪录 · Lucas Tenbrock弃踢手竞逐先发 · 宾州预算首推绩效拨款 · 超高性能混凝土降本75%"
THEME_EN = "Bellisario Doc Croatia Premiere · Ag Progress Days AI · Record $663M Fundraising · Swedish Punter Tenbrock · Performance-Based Funding · UHPC Cost Cut 75%"

#######################
# 1. BUILD NEWS CARDS
#######################

# Card 1: 传媒学院
card1 = """        <!-- 1. 传媒学院 -->
    <article class="news-card" id="news-1">
      <span class="card-tag tag-comm">传媒学院</span>
      <div class="card-body">
        <h2 class="card-title">Bellisario 副教授 Boaz Dvir 纪录片《To Kill a Nazi》克罗地亚国际电影节首映：7/27 在 17 世纪海景古堡公映</h2>
        <div class="card-title-en">Bellisario College professor Boaz Dvir's critically acclaimed documentary "To Kill a Nazi" makes international debut July 27 at Croatian International Film Festival · Penn State News</div>
        <div class="card-image"><img src="https://psu-gatsby-files-prod.s3.amazonaws.com/s3fs-public/styles/16_9_1000w/public/2026/07/boaddvir-redcarpet.jpg?h=b8aae163&amp;itok=CGGg4dF4" alt="" loading="lazy" onerror="this.parentElement.style.display='none'"></div>
        <p class="card-summary">
          <strong>核心提炼：</strong>Bellisario 学院<strong>新闻学副教授 Boaz Dvir</strong>（大屠杀幸存者后裔）执导、编剧并制作的纪录片<strong>《To Kill a Nazi》</strong>将于<strong>7 月 27 日</strong>在<strong>克罗地亚国际电影节</strong>（Šibenik）进行国际首映，放映地点为俯瞰<strong>亚得里亚海的 17 世纪 Barone 古堡</strong>。该片讲述法国男子 <strong>Michel Cojot 刺杀其父亲盖世太保行刑者的真实故事</strong>，探讨<strong>复仇、救赎与记忆</strong>等普世主题。旁白由著名演员 <strong>Jason Alexander</strong>（《宋飞正传》George Costanza）担任。该片已在<strong>好莱坞中国剧院</strong>「Dances With Films」影展获<strong>荣誉提名奖</strong>，并由国际发行商 <strong>Go2Films 签下销售协议</strong>。Forbes 影评人 Josh Weiss 称该片「仿佛畅销间谍惊悚小说」；《Forward》称其主题「具有无限的时效性」。Dvir 也是 Penn State 大屠杀、种族灭绝与人权教育计划的创始人与主任，当天将在电影节行业沙龙举办<strong>「挖掘野性故事」</strong>策展讲座。
        </p>
        <div class="card-meta">
          <div class="meta-left">
            <span class="psu source-badge">Penn State News</span>
          </div>
          <div class="meta-right">
            <span class="card-date">2026年7月16日</span>
          </div>
        </div>
        <a class="card-link" href="https://www.psu.edu/news/bellisario-college-communications/story/professors-documentary-make-international-debut-17th" target="_blank" rel="noopener">阅读原文<span class="arrow">→</span></a>
      </div>
    </article>"""

# Card 2: 演出预告
card2 = """        <!-- 2. 演出预告 -->
    <article class="news-card" id="news-2">
      <span class="card-tag tag-up">演出预告</span>
      <div class="card-body">
        <h2 class="card-title">Penn State 2026 Ag Progress Days 8/11-13 免费开展：TILVA AI 农业助手首秀 + 禽流感防控 + 斑衣蜡蝉最新动态</h2>
        <div class="card-title-en">Ag Progress Days Aug 11-13: Penn State Extension unveils TILVA AI assistant for agriculture, plus animal health updates on avian flu and spotted lanternfly · Penn State News</div>
        <div class="card-image"><img src="https://psu-gatsby-files-prod.s3.amazonaws.com/s3fs-public/styles/16_9_1000w/public/2026/07/apdcollegebuilding.png?h=6eb229a4&amp;itok=jTz_Cu9P" alt="" loading="lazy" onerror="this.parentElement.style.display='none'"></div>
        <p class="card-summary">
          <strong>核心提炼：</strong>Penn State <strong>2026 年 Ag Progress Days</strong>（农业进步日）将于<strong> 8 月 11 日至 13 日</strong>在<strong> Russell E. Larson 农业研究中心</strong>（Rock Springs，距 State College 9 英里）举行，<strong>免门票、免停车费</strong>。本届最大亮点：Penn State Extension 将首次公开演示 <strong>TILVA——农业 AI 助手</strong>，用户可上传照片识别<strong>病虫害与植物</strong>，获取结合实时天气与土壤条件的<strong>本地化推荐</strong>。农学院展览馆将集中展示<strong>「Technology for Agriculture and Living Systems (TALIS)」</strong>跨学科创新计划成果：作物育种的<strong>生物技术</strong>、果树种植的<strong>机器人精准施肥灌溉</strong>、支持保育的<strong>高级监测传感技术</strong>。动物健康展区将更新<strong>高致病性禽流感</strong>最新研究与防控最佳实践，并提供<strong>兽医与动物农业职业发展资讯</strong>。每天上午 11:00 设<strong>「新世界螺旋蝇美国发现：畜牧养殖者须知」</strong>主题演讲。开放时间：8/11 9:00-17:00；8/12 9:00-19:00；8/13 9:00-15:00。社交媒体标签 #agprogressdays。
        </p>
        <div class="card-meta">
          <div class="meta-left">
            <span class="psu source-badge">Penn State News</span>
          </div>
          <div class="meta-right">
            <span class="card-date">2026年7月10日</span>
          </div>
        </div>
        <a class="card-link" href="https://www.psu.edu/news/agricultural-sciences/story/ag-progress-days-showcases-college-research-ai-tool-and-animal-health" target="_blank" rel="noopener">阅读原文<span class="arrow">→</span></a>
      </div>
    </article>"""

# Card 3: 校友活动
card3 = """        <!-- 3. 校友活动 -->
    <article class="news-card" id="news-3">
      <span class="card-tag tag-alumni">校友活动</span>
      <div class="card-body">
        <h2 class="card-title">Penn State 年度筹款突破 6.63 亿美元创历史新高，24.1 万捐赠者同刷纪录，为 2027 年公开募资战役蓄势</h2>
        <div class="card-title-en">Penn State breaks fundraising records with $662.7M in FY 2025-26 — all-time high 241K donors ahead of public campaign launch in 2027 · Penn State News</div>
        <div class="card-image"><img src="https://psu-gatsby-files-prod.s3.amazonaws.com/s3fs-public/styles/16_9_1000w/public/2022/09/22%208%203-Hintz%20Lawn.jpg?h=84071268&amp;itok=afoYmNKb" alt="" loading="lazy" onerror="this.parentElement.style.display='none'"></div>
        <p class="card-summary">
          <strong>核心提炼：</strong>截至<strong> 6 月 30 日</strong>结束的 2025-26 财年，Penn State 获得<strong> 6.627 亿美元</strong>新捐赠，<strong>刷新此前 5.635 亿美元的校史纪录</strong>；同时捐赠者总数达到<strong>近 24.1 万人</strong>，校友会会员<strong> 176,356 人</strong>逼近历史峰值。校董会主席 <strong>David M. Kleppinger</strong> 称「这一成功为更宏大的募资战役奠定基础」——<strong> 2027 年将正式启动 Penn State 迄今最大规模公开募资</strong>，围绕<strong>学生教育转型、世界级科研、医疗保健、土地赠予使命</strong>五大核心方向。标志性捐赠包括：<strong> Tom Golisano 5000 万美元</strong>冠名儿童医院；匿名夫妇 <strong>5500 万美元遗产承诺</strong>资助宾州学生奖学金；Jonathan Wolf 设立<strong>成瘾与康复专业奖学金</strong>（获 2026 年度慈善家奖）；Clark 基金会 <strong>追加 1100 万美元</strong>续力工程学院 Clark 学者项目；已故 Snowiss 夫妇 <strong>1175 万美元遗产</strong>惠及 Palmer 美术馆与本科奖学金。小额定捐同样亮眼——<strong> 40.2 万笔千元以下捐赠</strong>，GivingTuesday 单日<strong>筹得 150 万美元+</strong>，THON 2026 <strong>1880 万美元再破纪录</strong>。平均每笔捐赠 1,060 美元。
        </p>
        <div class="card-meta">
          <div class="meta-left">
            <span class="psu source-badge">Penn State News</span>
          </div>
          <div class="meta-right">
            <span class="card-date">2026年7月16日</span>
          </div>
        </div>
        <a class="card-link" href="https://www.psu.edu/news/development-and-alumni-relations/story/penn-state-breaks-fundraising-records-accelerates-campaign" target="_blank" rel="noopener">阅读原文<span class="arrow">→</span></a>
      </div>
    </article>"""

# Card 4: 体育动态
card4 = """        <!-- 4. 体育动态 -->
    <article class="news-card" id="news-4">
      <span class="card-tag tag-sports">体育动态</span>
      <div class="card-body">
        <h2 class="card-title">SI：瑞典 6 尺 6 寸弃踢手 Lucas Tenbrock 正式入队，八月训练营将挑战先发位置</h2>
        <div class="card-title-en">Meet Penn State freshman punter Lucas Tenbrock — the 6-6 Swedish-born specialist who could contend for the starting job this fall · Sports Illustrated</div>
        <div class="card-image"><img src="https://images2.minutemediacdn.com/image/upload/c_crop,x_0,y_224,w_4760,h_2677/c_fill,w_1440,ar_1440:810,f_auto,q_auto,g_auto/images/ReutersImages/mmsport/all_penn_state/01kwyn0grpn9v9hqpxe3.jpg" alt="" loading="lazy" onerror="this.parentElement.style.display='none'"></div>
        <p class="card-summary">
          <strong>核心提炼：</strong>Sports Illustrated 聚焦 Penn State 2026 级<strong>弃踢手（Punter）Lucas Tenbrock</strong>——这位来自<strong>伊利诺伊州 St. Charles North 高中</strong>的<strong> 6 尺 6 寸（198cm）、210 磅（95kg）</strong>大一新生已正式加入球队名单，成为 2026 级<strong>第 12 位正式入队的签约生</strong>。Tenbrock 最初于<strong>去年 12 月签约 Matt Campbell 执教的 Iowa State</strong>，但在 Campbell 转投 PSU 后<strong>于 2 月随签 Penn State</strong>。他在高中时期<strong>两次当选 DuKane 联盟年度特勤组员</strong>，高三时弃踢 <strong>均码 43 码</strong>，附加分<strong> 42 罚 42 中</strong>，并带领全队<strong>成功执行 6 次 onside kick</strong>——被 247Sports Composite 评为<strong>全美第 5 号弃踢手、伊利诺伊州全州一阵</strong>。他还拥有<strong>进攻锋线经验</strong>，2024 年曾在 St. Charles North 担任<strong>右截锋先发</strong>，2025 年转为球队「第六锋线」专注弃踢。八月训练营将挑战<strong>密西西比州大转学生 Nathan Tiyce</strong>（6 尺 5、229 磅），争夺<strong>接替 Gabe Nwosu 成为新赛季先发弃踢手</strong>。文章还披露 <strong>2027 级长开球手 Clayton Powell</strong>和<strong> 2028 级踢球手 Carter Petri</strong>均已承诺加盟，Campbell 持续打造特勤组深度。
        </p>
        <div class="card-meta">
          <div class="meta-left">
            <span class="source-badge">Sports Illustrated</span>
          </div>
          <div class="meta-right">
            <span class="card-date">2026年7月7日</span>
          </div>
        </div>
        <a class="card-link" href="https://www.si.com/college/pennstate/football/meet-the-new-penn-state-freshman-who-could-contend-for-starting-spot-in-2026" target="_blank" rel="noopener">阅读原文<span class="arrow">→</span></a>
      </div>
    </article>"""

# Card 5: 行政人事
card5 = """        <!-- 5. 行政人事 -->
    <article class="news-card" id="news-5">
      <span class="card-tag tag-admin">行政人事</span>
      <div class="card-body">
        <h2 class="card-title">宾州 2026-27 预算首次引入绩效拨款模式：PSU 获追加 400 万美元+，教育拨款总额突破 2.46 亿</h2>
        <div class="card-title-en">Pennsylvania adopts performance-based funding for state-related universities: Penn State to receive $4M+ in new allocation under 2026-27 budget · Penn State News</div>
        <div class="card-image"><img src="https://psu-gatsby-files-prod.s3.amazonaws.com/s3fs-public/styles/16_9_1000w/public/2026/01/capitol-pa.jpg?h=6eb229a4&amp;itok=wbbwPJDh" alt="" loading="lazy" onerror="this.parentElement.style.display='none'"></div>
        <p class="card-summary">
          <strong>核心提炼：</strong>宾夕法尼亚州议会<strong> 2026-27 财年预算</strong>首次纳入<strong>绩效拨款（Performance-Based Funding）</strong>机制，为 Penn State、Pitt 和 Temple 三所州关联大学设立<strong> 1000 万美元专项池</strong>，PSU 预计获得<strong> 400 万美元以上追加</strong>——这是自<strong> 2019-20 财年以来</strong> PSU <strong>首次获得州教育拨款增长</strong>，总额超<strong> 2.46 亿美元</strong>（含 2.421 亿常规拨款）。校内评价校长 <strong>Neeli Bendapudi</strong> 称「绩效拨款模式的指标与 Penn State 的使命和价值观高度契合」；政府关系 VP <strong>Mike Stefan</strong> 表示「希望这是迈向更稳定年度拨款增长的第一步」。绩效指标涵盖<strong>宾州全日制本科生、Pell Grant 受助者、社区学院转学生入学人数</strong>以及<strong>毕业率、高需求学位产出、可负担性</strong>等。预算还包括：农业研究与推广 <strong>5770 万美元</strong>；Pennsylvania College of Technology <strong>3567 万美元</strong>；Invent Penn State <strong>235 万美元</strong>——均为平级拨款。该预算已提交<strong>州长 Josh Shapiro 签署</strong>。
        </p>
        <div class="card-meta">
          <div class="meta-left">
            <span class="psu source-badge">Penn State News</span>
          </div>
          <div class="meta-right">
            <span class="card-date">2026年7月12日</span>
          </div>
        </div>
        <a class="card-link" href="https://www.psu.edu/news/administration/story/penn-state-receive-performance-based-funding-2026-27-state-budget" target="_blank" rel="noopener">阅读原文<span class="arrow">→</span></a>
      </div>
    </article>"""

# Card 6: 科研成果
card6 = """        <!-- 6. 科研成果 -->
    <article class="news-card" id="news-6">
      <span class="card-tag tag-research">科研成果</span>
      <div class="card-body">
        <h2 class="card-title">Cement and Concrete Composites：PSU 工程团队揭示超高性能混凝土「降本 75%」新设计路径，非金属纤维或成关键</h2>
        <div class="card-title-en">New design approach may help slash the price of ultra-durable concrete by up to 75% — optimizing fiber volume, type and bond strength · Penn State Research, Cement and Concrete Composites</div>
        <div class="card-image"><img src="https://psu-gatsby-files-prod.s3.amazonaws.com/s3fs-public/styles/16_9_1000w/public/2026/06/untitled-1.jpg?h=84071268&amp;itok=ux-GtNTy" alt="" loading="lazy" onerror="this.parentElement.style.display='none'"></div>
        <p class="card-summary">
          <strong>核心提炼：</strong>Penn State <strong>土木与环境工程系</strong>主任 <strong>Farshad Rajabipour</strong>（John and Harriette Shaw 教授）课题组在《<strong>Cement and Concrete Composites</strong>》发表突破性研究：通过系统测试 15 种不同配方的<strong>超高性能混凝土（UHPC）</strong>，团队首次<strong>量化了各关键参数对性能与成本的影响</strong>，为将 UHPC 价格<strong>降低高达 75%</strong>提供了清晰设计路径。UHPC 比传统混凝土强度与韧性高出数十倍，但成本是后者的<strong> 30 倍</strong>——核心瓶颈在于内部的<strong>微钢纤维</strong>：仅占体积 2% 却贡献<strong>约 70% 的材料成本</strong>。团队关键发现：(1) <strong>微钢与条纹钢纤维</strong>即使体积减半仍能维持同等性能；(2) 纤维<strong>长径比越大</strong>拉伸性能越好；(3) <strong>工程化调控纤维-基体界面粘合力</strong>使纤维在断裂前「拔出」而非「瞬间折断」是维持韧性的关键；(4) 玻璃纤维、玄武岩纤维、碳/玻璃增强聚合物纤维虽目前性能不及钢，但<strong>更好的设计有望以几分之一成本实现钢级性能</strong>。Rajabipour 指出该研究使「混凝土生产商可以可靠自制 UHPC，不再受限于少数专有配方」——同时<strong>纤维也是最大碳排放来源</strong>，优化纤维可同步实现降本与减排。
        </p>
        <div class="card-meta">
          <div class="meta-left">
            <span class="source-badge">Penn State Research</span>
          </div>
          <div class="meta-right">
            <span class="card-date">2026年6月26日</span>
          </div>
        </div>
        <a class="card-link" href="https://www.psu.edu/news/research/story/new-design-approach-helps-slash-price-ultra-durable-concrete" target="_blank" rel="noopener">阅读原文<span class="arrow">→</span></a>
      </div>
    </article>"""

CARDS = [card1, card2, card3, card4, card5, card6]
TAGS = ["传媒学院", "演出预告", "校友活动", "体育动态", "行政人事", "科研成果"]

#######################
# 2. BUILD TODAY'S PAGE
#######################
src = os.path.join(ROOT, YESTERDAY_FILE)
dst = os.path.join(ROOT, TODAY_FILE)
shutil.copy2(src, dst)

with open(dst, 'r') as f:
    html = f.read()

# Replace date
html = html.replace("2026年7月17日 星期五", f"2026年7月18日 {WEEKDAY}")
html = html.replace("2026年7月17日", "2026年7月18日")
# Replace edition
html = html.replace("第 22 期", f"第 {EDITION} 期")
# Replace theme
old_cn = "今日本期聚焦 · AI重塑广告 · Palmer「美国梦」艺术展 · 2027杰出校友提名 · 橄榄球招募中期复盘 · Altoona新任副院长 · MPS「守门人」抗阿尔茨海默"
old_en = "Today's Focus · AI in Advertising · Palmer Museum Art · Distinguished Alumni · Football Recruiting Audit · Altoona Dean · MPS Alzheimer's Gatekeeper"
html = html.replace(old_cn, f"今日本期聚焦 · {THEME_CN}")
html = html.replace(old_en, f"Today's Focus · {THEME_EN}")

# Replace news cards
news_grid_start = html.find('<div class="news-grid">')
card6_pos = html.find('<!-- 6. 科研成果 -->')
close_div = html.find('</div>', card6_pos)
close_div2 = html.find('</div>', close_div + 6)

new_cards = '\n\n'.join(CARDS)
html = html[:news_grid_start + len('<div class="news-grid">')] + '\n\n' + new_cards + '\n\n  ' + html[close_div2:]

with open(dst, 'w') as f:
    f.write(html)

print(f"✅ Built {TODAY_FILE} (第 {EDITION} 期)")

# Verify minimum 6 news cards in today's file
with open(dst, 'r') as f:
    check = f.read()
card_count = check.count('class="news-card"')
print(f"  📊 {TODAY_FILE}: {card_count} news cards found")
assert card_count >= 6, f"ERROR: Only {card_count} cards in {TODAY_FILE}!"

#######################
# 3. UPDATE index.html
#######################
index_html = os.path.join(ROOT, 'index.html')
shutil.copy2(dst, index_html)
print("✅ Updated index.html from today's page")

#######################
# 4. UPDATE archive.html
#######################
archive_file = os.path.join(ROOT, 'archive.html')
with open(archive_file, 'r') as f:
    archive_html = f.read()

# Update count: increment all "共 N 期"
archive_html = re.sub(r'共 (\d+) 期', lambda m: f'共 {int(m.group(1)) + 1} 期', archive_html)

# The 6-keyword lead
lead_text = "Bellisario纪录片克罗地亚首映、Ag Progress Days农业AI展、捐赠6.63亿创纪录、Tenbrock弃踢手竞逐先发、宾州绩效拨款首落地、UHPC降本75%新路径"

# Prepend compact card before the first AUTO-APPEND-MARKER only
# The first marker is the one in the modern compact-card section
first_marker_pos = archive_html.find("<!-- AUTO-APPEND-MARKER - DO NOT REMOVE -->")
if first_marker_pos != -1:
    new_archive_card = f"""
        <a class="archive-card" href="{TODAY_FILE}">
          <div class="archive-date">2026.07.18 · 第 {EDITION} 期</div>
          <div class="archive-title">今日聚焦 · Bellisario纪录片克罗地亚首映</div>
          <div class="archive-lead">
            {', '.join(TAGS)} — {lead_text}
          </div>
        </a>
"""
    marker = "<!-- AUTO-APPEND-MARKER - DO NOT REMOVE -->"
    archive_html = archive_html[:first_marker_pos] + new_archive_card + '\n      ' + marker + archive_html[first_marker_pos + len(marker):]

with open(archive_file, 'w') as f:
    f.write(archive_html)
print("✅ Updated archive.html")

#######################
# 5. UPDATE archive-catalog.html
#######################
catalog_file = os.path.join(ROOT, 'archive-catalog.html')
with open(catalog_file, 'r') as f:
    cat_html = f.read()

cat_ids = ['cat-传媒学院', 'cat-演出预告', 'cat-校友活动', 'cat-体育动态', 'cat-行政人事', 'cat-科研成果']

for idx, cat_id in enumerate(cat_ids):
    # Find section
    section_start = cat_html.find(f'id="{cat_id}"')
    if section_start == -1:
        print(f"  ⚠️  Could not find section {cat_id}")
        continue
    
    # Update count: pattern like "22 条"
    count_match = re.search(r'(<span class="count">)(\d+)( 条</span>)', cat_html[section_start:section_start+200])
    if count_match:
        old_count = int(count_match.group(2))
        new_count = old_count + 1
        abs_start = section_start + count_match.start()
        cat_html = cat_html[:abs_start] + count_match.group(1) + str(new_count) + count_match.group(3) + cat_html[abs_start + len(count_match.group(0)):]
        print(f"  📊 {cat_id}: {old_count} → {new_count} 条")
    
    # Prepend entry to news-list
    news_list_marker = '<div class="news-list">'
    nl_start = cat_html.find(news_list_marker, section_start)
    if nl_start != -1:
        insert_pos = nl_start + len(news_list_marker)
        new_entry = f"""
          <a class="news-item" href="{TODAY_FILE}#news-{idx+1}">
            <span class="item-date">7/18</span>
            <span class="item-title">第{EDITION}期 · {TAGS[idx]}</span>
          </a>"""
        cat_html = cat_html[:insert_pos] + new_entry + cat_html[insert_pos:]

with open(catalog_file, 'w') as f:
    f.write(cat_html)
print("✅ Updated archive-catalog.html")

#######################
# 6. UPDATE history.json
#######################
history_file = os.path.join(ROOT, 'history.json')
with open(history_file, 'r') as f:
    history = json.load(f)

new_entries = [
    {"url": "https://www.psu.edu/news/bellisario-college-communications/story/professors-documentary-make-international-debut-17th", "title_cn": "Bellisario副教授Boaz Dvir纪录片\u300cTo Kill a Nazi\u300d克罗地亚国际电影节首映", "category": "传媒学院", "source": "Penn State News", "date": "2026-07-18"},
    {"url": "https://www.psu.edu/news/agricultural-sciences/story/ag-progress-days-showcases-college-research-ai-tool-and-animal-health", "title_cn": "2026 Ag Progress Days 8/11-13免费开展：TILVA AI农业助手首秀", "category": "演出预告", "source": "Penn State News", "date": "2026-07-18"},
    {"url": "https://www.psu.edu/news/development-and-alumni-relations/story/penn-state-breaks-fundraising-records-accelerates-campaign", "title_cn": "Penn State年度筹款突破6.63亿美元创历史新高", "category": "校友活动", "source": "Penn State News", "date": "2026-07-18"},
    {"url": "https://www.si.com/college/pennstate/football/meet-the-new-penn-state-freshman-who-could-contend-for-starting-spot-in-2026", "title_cn": "SI：瑞典弃踢手Lucas Tenbrock正式入队，八月竞逐先发", "category": "体育动态", "source": "Sports Illustrated", "date": "2026-07-18"},
    {"url": "https://www.psu.edu/news/administration/story/penn-state-receive-performance-based-funding-2026-27-state-budget", "title_cn": "宾州2026-27预算首推绩效拨款：PSU获追加400万+美元", "category": "行政人事", "source": "Penn State News", "date": "2026-07-18"},
    {"url": "https://www.psu.edu/news/research/story/new-design-approach-helps-slash-price-ultra-durable-concrete", "title_cn": "Cement and Concrete Composites：UHPC降本75%新设计路径", "category": "科研成果", "source": "Penn State Research", "date": "2026-07-18"},
]

for entry in new_entries:
    history['shown_news_history'].append(entry)

history['last_updated'] = TODAY

with open(history_file, 'w') as f:
    json.dump(history, f, ensure_ascii=False, indent=2)
print(f"✅ Updated history.json ({len(history['shown_news_history'])} entries)")

# Verify JSON validity
with open(history_file, 'r') as f:
    json.load(f)
print("✅ history.json JSON is valid")

# Final verification — count cards in index.html
with open(os.path.join(ROOT, 'index.html'), 'r') as f:
    idx_cards = f.read().count('class="news-card"')
print(f"\n🎉 Build complete for 2026-07-18 (第 {EDITION} 期)!")
print(f"📊 Cards: daily={card_count}, index={idx_cards}")
print("Next steps: git add, commit, push")
