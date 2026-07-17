#!/usr/bin/env python3
"""Build PSU Daily News for 2026-07-17 — 第 22 期"""
import json, shutil, os, re

ROOT = "/Users/mac/WorkBuddy/2026-06-25-12-43-57/psu-news-daily"
TODAY = "2026-07-17"
YESTERDAY = "2026-07-15"  # 7/16 missing
TODAY_FILE = f"psu-news-{TODAY}.html"
YESTERDAY_FILE = f"psu-news-{YESTERDAY}.html"
EDITION = "22"
WEEKDAY = "星期五"
THEME_CN = "AI重塑广告 · Palmer「美国梦」艺术展 · 2027杰出校友提名 · 橄榄球招募中期复盘 · Altoona新任副院长 · MPS「守门人」抗阿尔茨海默"
THEME_EN = "AI in Advertising · Palmer Museum Art · Distinguished Alumni · Football Recruiting Audit · Altoona Dean · MPS Alzheimer's Gatekeeper"

#######################
# 1. BUILD NEWS CARDS
#######################

# Card 1: 传媒学院
card1 = """        <!-- 1. 传媒学院 -->
    <article class="news-card" id="news-1">
      <span class="card-tag tag-comm">传媒学院</span>
      <div class="card-body">
        <h2 class="card-title">Bellisario 助理教授 Yujin Heo 重新思考 AI 在广告中的角色：以更少伤害、更负责任的方式使用人工智能</h2>
        <div class="card-title-en">Bellisario College professor rethinks AI's role in advertising — exploring socially responsible, less harmful applications of artificial intelligence · Penn State News</div>
        <div class="card-image"><img src="https://psu-gatsby-files-prod.s3.amazonaws.com/s3fs-public/styles/16_9_1000w/public/2026/07/yujinheo-bellisariocollege26.jpg?h=f16d09b5&itok=obokKHm7" alt="" loading="lazy" onerror="this.parentElement.style.display='none'"></div>
        <p class="card-summary">
          <strong>核心提炼：</strong>Bellisario 学院广告/公关系<strong>助理教授 Yujin Heo</strong>以独特视角研究 AI——她关注的不是效率提升，而是<strong>如何让 AI 以更少伤害、更具社会责任感的方式服务广告业</strong>。在近期一项研究中，Heo 比较了<strong>AI 时尚模特与真人模特</strong>对消费者的影响：真人模特触发身材比较、降低身体自尊，<strong>AI 标记模特则不产生这种负面效应</strong>——暗示 AI 可能成为「伤害更小的替代方案」。另一项研究发现，<strong>AI 虚拟网红</strong>在丑闻情境下表现优于真人网红，且无丑闻时二者效果相当，从<strong>危机管理角度</strong>这可能使品牌考虑使用虚拟代言人。Heo 于 2023 年从南卡大学获博士学位后加入 Penn State，任教 COMM 420（研究方法）和 COMM 450A（数字营销），系主任 Fuyuan Shen 评价她「一位人人都希望在团队中拥有的可靠且富有洞察力的同事」。
        </p>
        <div class="card-meta">
          <div class="meta-left">
            <span class="psu source-badge">Penn State News</span>
          </div>
          <div class="meta-right">
            <span class="card-date">2026年7月14日</span>
          </div>
        </div>
        <a class="card-link" href="https://www.psu.edu/news/bellisario-college-communications/story/bellisario-college-professor-rethinks-ais-role-advertising" target="_blank" rel="noopener">阅读原文<span class="arrow">→</span></a>
      </div>
    </article>"""

# Card 2: 演出预告
card2 = """        <!-- 2. 演出预告 -->
    <article class="news-card" id="news-2">
      <span class="card-tag tag-up">演出预告</span>
      <div class="card-body">
        <h2 class="card-title">Palmer 美术馆「Dreaming American Futures」大型群展展出至 11/29，50 位当代艺术家回应「何为美国人」</h2>
        <div class="card-title-en">Palmer Museum of Art's "Dreaming American Futures: Invitational 250" features 59 works by 50 artists, on view through Nov. 29 · Penn State News</div>
        <div class="card-image"><img src="https://psu-gatsby-files-prod.s3.amazonaws.com/s3fs-public/styles/16_9_1000w/public/2026/06/heidi-4x3.jpg?h=60b3920b&itok=L8Kp7_D5" alt="" loading="lazy" onerror="this.parentElement.style.display='none'"></div>
        <p class="card-summary">
          <strong>核心提炼：</strong>Penn State <strong>Palmer 美术馆</strong>正在举办<strong>「Dreaming American Futures: Invitational 250」</strong>大型评审邀请展，<strong>展期至 11 月 29 日</strong>，免费开放。展览恰逢美国<strong>独立宣言签署 250 周年</strong>纪念，特邀 <strong>50 位当代艺术家</strong>（含 Penn State 学生、教职员工、宾州校友及 State College 周边 50 英里内艺术家）提交 59 件作品，涵盖<strong>绘画、雕塑、陶瓷、摄影、混合媒介、纸上作品</strong>等。评审团从<strong>近 300 件投稿</strong>中精选，四大主题贯穿全展：<strong>「激活变革」「弥合分歧」「追求幸福」「更完美的联邦」</strong>。Penn State Altoona 校区<strong>人类发展与家庭研究系助理教授 Heidi Manfred</strong>的油画「Secure and Moving Forward」入选，以交织色块与圆形象征<strong>社会团结与韧性</strong>。馆长 Amanda Hellman 称这是 Palmer 首次举办公开征件的评审展，体现「of the people, by the people」精神。
        </p>
        <div class="card-meta">
          <div class="meta-left">
            <span class="psu source-badge">Penn State News</span>
          </div>
          <div class="meta-right">
            <span class="card-date">2026年6月16日</span>
          </div>
        </div>
        <a class="card-link" href="https://www.psu.edu/news/altoona/story/penn-state-altoona-professor-featured-new-palmer-museum-art-exhibition" target="_blank" rel="noopener">阅读原文<span class="arrow">→</span></a>
      </div>
    </article>"""

# Card 3: 校友活动
card3 = """        <!-- 3. 校友活动 -->
    <article class="news-card" id="news-3">
      <span class="card-tag tag-alumni">校友活动</span>
      <div class="card-body">
        <h2 class="card-title">Penn State 2027 杰出校友奖提名正式开放，9 月 30 日截止，11 月校董会评审</h2>
        <div class="card-title-en">Nominations sought for 2027 Distinguished Alumni Awards — Penn State's highest alumni honor, deadline Sept. 30 · Penn State News</div>
        <div class="card-image"><img src="https://psu-gatsby-files-prod.s3.amazonaws.com/s3fs-public/styles/16_9_1000w/public/2023/02/Nittany%20Lion%20Shrine.jpg?h=a8697ad7&itok=300Kewud" alt="" loading="lazy" onerror="this.parentElement.style.display='none'"></div>
        <p class="card-summary">
          <strong>核心提炼：</strong>Penn State 正式启动<strong> 2027 年杰出校友奖（Distinguished Alumni Award）</strong>提名征集。该奖项由校董会于<strong> 1951 年授权设立</strong>，是 Penn State 授予校友的<strong>最高荣誉</strong>，表彰「个人生活、职业成就和社区服务体现母校宗旨」的在世校友。现任校董会成员、在校雇员、校友会执行委员会成员不可获提名。<strong>提名截止日期为 9 月 30 日</strong>，提名表提交至 <strong>dku5025@psu.edu</strong>。校董会筛选委员会将根据提名表确定推荐人选，<strong>2026 年 11 月校董会会议</strong>以投票方式最终选出 2027 年度获奖者。往届获奖名单可在校友会官网查阅。此次提名面向全球 <strong>80 万+ 校友</strong>，是 Penn State 表彰校友社会贡献的最高规格年度传统。
        </p>
        <div class="card-meta">
          <div class="meta-left">
            <span class="psu source-badge">Penn State News</span>
          </div>
          <div class="meta-right">
            <span class="card-date">2026年7月15日</span>
          </div>
        </div>
        <a class="card-link" href="https://www.psu.edu/news/alumni/story/nominations-sought-2027-distinguished-alumni-awards" target="_blank" rel="noopener">阅读原文<span class="arrow">→</span></a>
      </div>
    </article>"""

# Card 4: 体育动态
card4 = """        <!-- 4. 体育动态 -->
    <article class="news-card" id="news-4">
      <span class="card-tag tag-sports">体育动态</span>
      <div class="card-body">
        <h2 class="card-title">SI 深度复盘：Penn State 2027 招募班「得失录」——瑞典 6 尺 8 寸锋线新星加盟，Big Ten 排名从第一跌至第七</h2>
        <div class="card-title-en">The Hits and Misses of Penn State's 2027 Recruiting Class: Swedish OL Oscar Webersink commits, but class drops from No. 1 Big Ten to 7th · Sports Illustrated</div>
        <div class="card-image"><img src="https://images2.minutemediacdn.com/image/upload/c_crop,x_0,y_75,w_4304,h_2421/c_fill,w_1440,ar_1440:810,f_auto,q_auto,g_auto/images/ReutersImages/mmsport/all_penn_state/01kx1rrtn0bgcg1f0v3r.jpg" alt="" loading="lazy" onerror="this.parentElement.style.display='none'"></div>
        <p class="card-summary">
          <strong>核心提炼：</strong>Sports Illustrated 对 Penn State <strong>2027 届橄榄球招募</strong>进行全面复盘。<strong>亮点：</strong>新近签约的<strong>瑞典进攻锋线 Oscar Webersink</strong>（6 尺 8 寸/290 磅）是一位<strong>仅接触美式足球两年的「隐藏宝石」</strong>，Campbell 教练看中其<strong>移动能力与高天花板潜力</strong>；现有 20 名承诺中含 6 名四星——防守截锋 <strong>Stanley Montgomery</strong>、角卫 <strong>Kei'Shjuan Telfair</strong>（全美前 100）、进攻截锋 <strong>David Tarawallie</strong>；四分卫已锁定马萨诸塞州三星 <strong>Will Wood</strong>。<strong>不足：</strong>六周前还是 <strong>Big Ten 第一</strong>的招募班，因接连遭遇多名四星级球员解约（Aiden Gibson→Rutgers、Jamir Dean、Khalil Taylor→Nebraska），排名骤降至<strong>全美第 20、Big Ten 第 7</strong>；<strong>宾州本土前 20 名仅签下 1 人</strong>；无 WR 外接手进入全美前 200。SI 分析认为 Campbell 定位为「球员发展型教练」，本届招募的真正评判要看 <strong>2028 届及首个赛季战绩</strong>。
        </p>
        <div class="card-meta">
          <div class="meta-left">
            <span class="source-badge">Sports Illustrated</span>
          </div>
          <div class="meta-right">
            <span class="card-date">2026年7月14日</span>
          </div>
        </div>
        <a class="card-link" href="https://www.si.com/college/pennstate/football/the-hits-and-misses-of-penn-state-2027-recruiting-class-so-far" target="_blank" rel="noopener">阅读原文<span class="arrow">→</span></a>
      </div>
    </article>"""

# Card 5: 行政人事
card5 = """        <!-- 5. 行政人事 -->
    <article class="news-card" id="news-5">
      <span class="card-tag tag-admin">行政人事</span>
      <div class="card-body">
        <h2 class="card-title">Jungwoo Ryoo 出任 Penn State Altoona 成人教育副院长：前 DuBois 校区校长回归 Altoona</h2>
        <div class="card-title-en">Jungwoo Ryoo named associate dean for adult education at Penn State Altoona, transitioning from DuBois chancellor role · Penn State News</div>
        <div class="card-image"><img src="https://psu-gatsby-files-prod.s3.amazonaws.com/s3fs-public/styles/16_9_1000w/public/2026/07/jungwoo-ryoo-headshot.jpg?h=a50e510a&itok=VoPkomws" alt="" loading="lazy" onerror="this.parentElement.style.display='none'"></div>
        <p class="card-summary">
          <strong>核心提炼：</strong>Penn State 任命 <strong>Jungwoo Ryoo</strong> 为 <strong>Penn State Altoona 校区成人教育副院长（Associate Dean for Adult Education）</strong>，将于<strong> 2027 年 7 月</strong>正式履新。Ryoo 目前担任 <strong>Penn State DuBois 校区校长兼首席学术官（CAO）</strong>，此前于 2015-2022 年任 Altoona 校区<strong>商业工程与 IST 学部主任</strong>，此次是「回归 Altoona」。他在 DuBois 期间主导推出<strong> Industry 4.0 学院</strong>（通过 LaunchBox 向 K-12 学生与成人介绍自动化、机器人、AI 与网安），并推动<strong>三县地区粉末冶金制造业复兴</strong>。Ryoo 表示新岗位的核心使命是<strong>「拓宽 Penn State 学生的定义，纳入非传统学习者」</strong>——通过灵活的学位路径回应劳动力需求、拓展招生与资源活力。他本人拥有<strong>军队战斗医护兵背景</strong>并曾在全职工作期间完成博士学位，对成人学习者「边工作边读书」的挑战有切身体会。
        </p>
        <div class="card-meta">
          <div class="meta-left">
            <span class="psu source-badge">Penn State News</span>
          </div>
          <div class="meta-right">
            <span class="card-date">2026年7月15日</span>
          </div>
        </div>
        <a class="card-link" href="https://www.psu.edu/news/altoona/story/jungwoo-ryoo-named-associate-dean-adult-education-penn-state-altoona" target="_blank" rel="noopener">阅读原文<span class="arrow">→</span></a>
      </div>
    </article>"""

# Card 6: 科研成果
card6 = """        <!-- 6. 科研成果 -->
    <article class="news-card" id="news-6">
      <span class="card-tag tag-research">科研成果</span>
      <div class="card-body">
        <h2 class="card-title">Science Advances：大脑细胞隐藏「骨架守门人」或成阿尔茨海默早期干预新靶点</h2>
        <div class="card-title-en">Membrane-associated periodic skeleton acts as gatekeeper for brain cell endocytosis — MPS breakdown accelerates Alzheimer's amyloid buildup · Penn State Eberly College of Science</div>
        <div class="card-image"><img src="https://ecos-appdev-production.s3.amazonaws.com/science_site/s3fs-public/styles/f_story_hero/public/2026-02/2026_zhou-lab_20-copy.jpg?h=9896f5b6&itok=kLw1moh7" alt="" loading="lazy" onerror="this.parentElement.style.display='none'"></div>
        <p class="card-summary">
          <strong>核心提炼：</strong>Penn State <strong>Eberly 理学院</strong>周若波（Ruobo Zhou）课题组在《<strong>Science Advances</strong>》发表重磅成果：大脑神经元细胞膜下方存在一个<strong>由肌动蛋白和血影蛋白重复环构成的周期性骨架结构 MPS（membrane-associated periodic skeleton）</strong>，此前被认为仅起被动支撑作用，新研究证明它实际上是<strong>所有主要形式「胞吞作用」的物理守门人</strong>。团队使用<strong>超分辨率显微镜（纳米级成像）</strong>在培养神经元中追踪特定蛋白：当 MPS 被药物或基因手段破坏，内吞速率<strong>翻倍</strong>；更惊人的是发现<strong>正反馈回路</strong>——加速的内吞激活 calpain 蛋白酶切割骨架蛋白，骨架子结构自毁后进一步加速摄取。在模拟<strong>阿尔茨海默病早期</strong>的细胞模型中，MPS 削弱导致<strong>淀粉样前体蛋白（APP）过度内化，Aβ42 毒性片段累积增加 30-50%，神经元死亡标志物显著上升</strong>。周若波 2013 年在哈佛做博后时首次发现 MPS 结构，一作<strong>博士生 Jinyu Fei</strong>表示「保存或稳定 MPS 可能减缓阿尔茨海默症状出现前的早期细胞变化」。
        </p>
        <div class="card-meta">
          <div class="meta-left">
            <span class="source-badge">Penn State Science</span>
          </div>
          <div class="meta-right">
            <span class="card-date">2026年2月11日</span>
          </div>
        </div>
        <a class="card-link" href="https://science.psu.edu/news/skeleton-gatekeeper-lining-brain-cells-could-guard-against-alzheimers" target="_blank" rel="noopener">阅读原文<span class="arrow">→</span></a>
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
html = html.replace("2026年7月15日 星期三", f"2026年7月17日 {WEEKDAY}")
html = html.replace("2026年7月15日", "2026年7月17日")
# Replace edition
html = html.replace("第 21 期", f"第 {EDITION} 期")
# Replace theme
html = html.replace("今日本期聚焦 · 学生创意金奖 · 说唱传奇橄榄球周末 · FastStart 导师招募 · 2027 招募行情深度 · Sloan 高等教育奖 · PNAS 可涂鸦传感器", f"今日本期聚焦 · {THEME_CN}")
html = html.replace("Today's Focus · CommAgency Telly Gold · Lil Wayne BJC Football Weekend · FastStart Mentors · 2027 Recruiting Analysis · Sloan Education Award · Paintable Electrodes in PNAS", f"Today's Focus · {THEME_EN}")

# Replace news cards — find the <div class="news-grid"> block and replace everything between it and the closing </div>
# Use a marker approach
news_grid_start = html.find('<div class="news-grid">')
news_grid_end = html.find('</div>', html.find('<!-- 6. 科研成果 -->'))
# Find the actual end by locating </div> after card6
card6_pos = html.find('<!-- 6. 科研成果 -->')
close_div = html.find('</div>', card6_pos)
# Find the second </div> (first is likely inside the card)
close_div2 = html.find('</div>', close_div + 6)

new_cards = '\n\n'.join(CARDS)
html = html[:news_grid_start + len('<div class="news-grid">')] + '\n\n' + new_cards + '\n\n  ' + html[close_div2:]

# Fix source-badge classes — combine "psu" with "source-badge" into single class attr
# Pattern: <span class="psu source-badge"> -> <span class="psu source-badge">
# Actually need to check if we have double class attr issues
# In this file, cards use <span class="psu source-badge"> and <span class="source-badge"> patterns

with open(dst, 'w') as f:
    f.write(html)

print(f"✅ Built {TODAY_FILE} (第 {EDITION} 期)")

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

# Update count: "共 N 期"
archive_html = re.sub(r'共 (\d+) 期', lambda m: f'共 {int(m.group(1)) + 1} 期', archive_html)

# Prepend new card before AUTO-APPEND-MARKER
new_archive_card = f"""
        <a class="archive-card" href="{TODAY_FILE}">
          <div class="archive-date">2026.07.17 · 第 {EDITION} 期</div>
          <div class="archive-title">今日聚焦 · {THEME_CN.split('·')[1].strip() if '·' in THEME_CN else THEME_CN}</div>
          <div class="archive-lead">
            {', '.join(TAGS)} — AI广告伦理研究、Palmer「美国梦」群展、杰出校友提名启动、橄榄球招募中期复盘、Altoona 成人教育新副院长、MPS 骨架「守门人」抗阿尔茨海默
          </div>
        </a>
"""
marker = "<!-- AUTO-APPEND-MARKER - DO NOT REMOVE -->"
archive_html = archive_html.replace(marker, new_archive_card + '\n      ' + marker)

with open(archive_file, 'w') as f:
    f.write(archive_html)
print("✅ Updated archive.html")

#######################
# 5. UPDATE archive-catalog.html
#######################
catalog_file = os.path.join(ROOT, 'archive-catalog.html')
with open(catalog_file, 'r') as f:
    cat_html = f.read()

# For each category section, update count and prepend entry
# We need to find each cat-section and update
cat_names = {
    '传媒学院': ('bellisario', 'cat-bellisario'),
    '演出预告': ('events', 'cat-events'),
    '校友活动': ('alumni', 'cat-alumni'),
    '体育动态': ('sports', 'cat-sports'),
    '行政人事': ('admin', 'cat-admin'),
    '科研成果': ('research', 'cat-research'),
}

for idx, (cat_name, _) in enumerate(TAGS):
    # Find the section and update count
    # Each section has a pattern like "cat-bellisario" in the id
    cat_id = list(cat_names.values())[idx][1]
    
    # Update count: pattern like (5) -> (6) or （5篇）-> （6篇）
    # Search for patterns near cat_id
    section_start = cat_html.find(f'id="{cat_id}"')
    if section_start == -1:
        section_start = cat_html.find(f'id="cat-')
    
    # Find the count span
    count_pattern = r'(<span class="count">)(\d+)(</span>)'
    # Replace first occurrence after section_start
    match = re.search(count_pattern, cat_html[section_start:])
    if match:
        old_count = int(match.group(2))
        new_count = old_count + 1
        cat_html = cat_html[:section_start + match.start()] + \
                    match.group(1) + str(new_count) + match.group(3) + \
                    cat_html[section_start + match.end():]
    
    # Prepend entry to news-list
    news_list_marker = '<div class="news-list">'
    nl_start = cat_html.find(news_list_marker, section_start)
    if nl_start != -1:
        insert_pos = nl_start + len(news_list_marker)
        new_entry = f"""
          <a class="news-item" href="{TODAY_FILE}#news-{idx+1}">
            <span class="item-date">7/17</span>
            <span class="item-title">第{EDITION}期 · {cat_name}</span>
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
    {
        "url": "https://www.psu.edu/news/bellisario-college-communications/story/bellisario-college-professor-rethinks-ais-role-advertising",
        "title_cn": "Bellisario 助理教授 Yujin Heo 重新思考 AI 在广告中的角色",
        "category": "传媒学院",
        "source": "Penn State News",
        "date": "2026-07-17"
    },
    {
        "url": "https://www.psu.edu/news/altoona/story/penn-state-altoona-professor-featured-new-palmer-museum-art-exhibition",
        "title_cn": "Palmer 美术馆「Dreaming American Futures」大型群展",
        "category": "演出预告",
        "source": "Penn State News",
        "date": "2026-07-17"
    },
    {
        "url": "https://www.psu.edu/news/alumni/story/nominations-sought-2027-distinguished-alumni-awards",
        "title_cn": "Penn State 2027 杰出校友奖提名正式开放",
        "category": "校友活动",
        "source": "Penn State News",
        "date": "2026-07-17"
    },
    {
        "url": "https://www.si.com/college/pennstate/football/the-hits-and-misses-of-penn-state-2027-recruiting-class-so-far",
        "title_cn": "SI 深度复盘 Penn State 2027 招募班「得失录」",
        "category": "体育动态",
        "source": "Sports Illustrated",
        "date": "2026-07-17"
    },
    {
        "url": "https://www.psu.edu/news/altoona/story/jungwoo-ryoo-named-associate-dean-adult-education-penn-state-altoona",
        "title_cn": "Jungwoo Ryoo 出任 Penn State Altoona 成人教育副院长",
        "category": "行政人事",
        "source": "Penn State News",
        "date": "2026-07-17"
    },
    {
        "url": "https://science.psu.edu/news/skeleton-gatekeeper-lining-brain-cells-could-guard-against-alzheimers",
        "title_cn": "Science Advances：大脑细胞隐藏「骨架守门人」或成阿尔茨海默早期干预新靶点",
        "category": "科研成果",
        "source": "Penn State Eberly College of Science",
        "date": "2026-07-17"
    }
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

print("\n🎉 Build complete for 2026-07-17 (第 22 期)!")
print("Next steps: git add, commit, push")
