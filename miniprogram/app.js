App({
  onLaunch() {
    // 初始化：检查网络、加载缓存
    this.checkUpdate()
  },

  checkUpdate() {
    const updateManager = wx.getUpdateManager()
    updateManager.onCheckForUpdate((res) => {
      if (res.hasUpdate) {
        updateManager.onUpdateReady(() => {
          wx.showModal({
            title: '更新提示',
            content: '新版本已准备好，是否重启？',
            success: (res) => {
              if (res.confirm) updateManager.applyUpdate()
            }
          })
        })
      }
    })
  },

  globalData: {
    apiBase: 'https://your-domain.com'  // 改成你的服务器域名
  }
})
