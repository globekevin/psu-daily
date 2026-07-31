// pages/index/index.js
const api = require('../../utils/api')

Page({
  data: {
    loading: true,
    cards: [],
    dateCN: '',
    weekday: '',
    edition: 0
  },

  onLoad() {
    this.loadNews()
  },

  onShow() {
    // 每次切回首页静默刷新
    if (!this.data.loading) {
      this.loadNews(false)
    }
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.loadNews(true)
  },

  /**
   * 加载新闻
   * @param {boolean} showLoading - 是否显示 loading 状态
   */
  async loadNews(showLoading = true) {
    if (showLoading) {
      this.setData({ loading: true })
    }
    try {
      const data = await api.fetchToday()
      // 处理摘要中的 <strong>、<br> 等 HTML 标签 → richtext nodes
      const cards = (data.cards || []).map((card) => ({
        ...card,
        summaryNodes: this.parseSummary(card.summary)
      }))

      this.setData({
        loading: false,
        cards,
        dateCN: data.date_cn || '',
        weekday: data.weekday || '',
        edition: data.edition || 0
      })
    } catch (err) {
      console.error('加载失败:', err)
      this.setData({ loading: false })
      wx.showToast({
        title: '加载失败，下拉重试',
        icon: 'none',
        duration: 2000
      })
    }
    wx.stopPullDownRefresh()
  },

  /**
   * 简单 HTML → richtext nodes 转换
   * 支持 <strong>、<br>、<p> 等基本标签
   */
  parseSummary(html) {
    if (!html) return []
    const nodes = []
    let pos = 0
    const len = html.length
    const tagRegex = /<(\/?)(\w+)[^>]*>/g
    let match
    let bold = false

    while ((match = tagRegex.exec(html)) !== null) {
      // 前面的文本
      if (match.index > pos) {
        const text = this.decodeHtml(html.slice(pos, match.index))
        if (text) {
          nodes.push({ type: 'text', text, ...(bold ? { bold: true } : {}) })
        }
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
    // 剩余文本
    if (pos < len) {
      const text = this.decodeHtml(html.slice(pos))
      if (text) {
        nodes.push({ type: 'text', text })
      }
    }
    return nodes
  },

  /**
   * HTML 实体解码
   */
  decodeHtml(str) {
    return str
      .replace(/&amp;/g, '&')
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>')
      .replace(/&quot;/g, '"')
      .replace(/&#x27;/g, "'")
      .replace(/&#(\d+);/g, (_, n) => String.fromCharCode(n))
  },

  /**
   * 点击卡片 → 复制链接或跳转详情
   */
  onTapCard(e) {
    const url = e.currentTarget.dataset.url
    const index = e.currentTarget.dataset.index
    // 复制原文链接（小程序内无法直接打开外部网页，除非配置了 webview 域名）
    wx.setClipboardData({
      data: url,
      success: () => {
        wx.showToast({
          title: '链接已复制，请在浏览器打开',
          icon: 'none',
          duration: 2500
        })
      }
    })
  }
})
