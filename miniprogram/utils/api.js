/**
 * PSU Daily News — API 请求工具
 * 所有接口统一走这里，方便切换环境、加缓存。
 */

// 注意: 不在模块顶层调 getApp()，避免 App 未初始化
function getBase() {
  const app = getApp()
  return app.globalData.apiBase
}

/**
 * 通用 GET 请求
 */
function get(path) {
  const base = getBase()
  return new Promise((resolve, reject) => {
    wx.request({
      url: `${base}${path}`,
      method: 'GET',
      header: { 'Content-Type': 'application/json' },
      timeout: 15000,
      success(res) {
        if (res.statusCode === 200) {
          resolve(res.data)
        } else {
          reject(res)
        }
      },
      fail(err) {
        reject(err)
      }
    })
  })
}

/**
 * 获取今日新闻（或最新一期）
 */
function fetchToday() {
  return get('/api/news/today')
}

/**
 * 获取指定日期的新闻
 * @param {string} date - "2026-07-31"
 */
function fetchDate(date) {
  return get(`/api/news/date/${date}`)
}

/**
 * 获取所有有数据的日期列表
 */
function fetchDates() {
  return get('/api/news/dates')
}

module.exports = {
  fetchToday,
  fetchDate,
  fetchDates
}
