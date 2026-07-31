// pages/detail/detail.js
Page({
  data: {
    titleCN: '',
    titleEN: '',
    category: '',
    tag_class: '',
    image: '',
    summaryNodes: [],
    source: '',
    dateCN: '',
    url: ''
  },

  onLoad(options) {
    // 从页面参数读取卡片数据
    const card = decodeURIComponent(options.card || '{}')
    try {
      const data = JSON.parse(card)
      this.setData({
        titleCN: data.title_cn || '',
        titleEN: data.title_en || '',
        category: data.category_cn || '',
        tag_class: data.tag_class || '',
        image: data.image || '',
        source: data.source || '',
        dateCN: data.date_cn || '',
        url: data.url || ''
      })

      // 解析摘要
      if (data.summary) {
        this.setData({ summaryNodes: this.parseSummary(data.summary) })
      }
    } catch (e) {
      console.error('卡片数据解析失败:', e)
    }
  },

  parseSummary(html) {
    // 同 index.js 中的 parseSummary 逻辑
    if (!html) return []
    const nodes = []
    let pos = 0, bold = false
    const tagRegex = /<(\/?)(\w+)[^>]*>/g
    let match

    while ((match = tagRegex.exec(html)) !== null) {
      if (match.index > pos) {
        const text = this.decodeHtml(html.slice(pos, match.index))
        if (text) nodes.push({ type: 'text', text, ...(bold ? { bold: true } : {}) })
      }
      const tag = match[2].toLowerCase()
      if (match[1] === '/') {
        if (tag === 'strong' || tag === 'b') bold = false
      } else {
        if (tag === 'strong' || tag === 'b') bold = true
        if (tag === 'br') nodes.push({ type: 'text', text: '\n' })
      }
      pos = tagRegex.lastIndex
    }
    if (pos < html.length) {
      const text = this.decodeHtml(html.slice(pos))
      if (text) nodes.push({ type: 'text', text })
    }
    return nodes
  },

  decodeHtml(str) {
    return str
      .replace(/&amp;/g, '&').replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>').replace(/&quot;/g, '"')
      .replace(/&#(\d+);/g, (_, n) => String.fromCharCode(n))
  },

  goBack() {
    wx.navigateBack()
  },

  openOriginal() {
    if (!this.data.url) return
    wx.setClipboardData({
      data: this.data.url,
      success: () => {
        wx.showToast({ title: '链接已复制，请用浏览器打开', icon: 'none', duration: 2500 })
      }
    })
  }
})
