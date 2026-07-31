#!/usr/bin/env python3
"""
PSU Daily News — FastAPI 后端服务
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
为微信小程序提供 JSON API。

启动: uvicorn main:app --host 0.0.0.0 --port 8000
生产: 前面套 nginx + HTTPS（小程序强制要求）
"""

import os
from datetime import date, datetime
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from news_engine import generate_news, load_daily, init_history, DATA_DIR

# ── Auth token for refresh endpoint ──
REFRESH_TOKEN = os.environ.get("REFRESH_TOKEN", "psu-daily-refresh-2026")

app = FastAPI(
    title="PSU Daily News API",
    description="宾州州立大学每日新闻 — 微信小程序后端",
    version="1.0.0",
)

# CORS: allow mini-program dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    init_history()


# ═══════════════════════════════════════════════════
#  API ROUTES
# ═══════════════════════════════════════════════════

@app.get("/")
def root():
    return {"service": "PSU Daily News API", "version": "1.0.0", "status": "running"}


@app.get("/api/news/today")
def get_today():
    """获取今日新闻（如今天还没生成，返回最新的）。"""
    data = load_daily()
    if not data:
        return JSONResponse(
            content={"error": "暂无新闻数据，请稍后再试"},
            status_code=404,
        )
    return data


@app.get("/api/news/date/{date_str}")
def get_by_date(date_str: str):
    """获取指定日期的新闻，格式: 2026-07-31"""
    data = load_daily(date_str)
    if not data:
        return JSONResponse(
            content={"error": f"{date_str} 无数据"},
            status_code=404,
        )
    return data


@app.get("/api/news/latest")
def get_latest():
    """获取最近一期新闻（即使不是今天）。"""
    data = load_daily()  # Falls back to latest
    if not data:
        return JSONResponse(
            content={"error": "暂无新闻数据"},
            status_code=404,
        )
    return data


@app.get("/api/news/dates")
def list_dates():
    """列出所有有数据的日期。"""
    files = sorted(DATA_DIR.glob("20*.json"), reverse=True)
    dates = [f.stem for f in files]
    return {"dates": dates, "count": len(dates)}


@app.post("/api/news/refresh")
def refresh(token: str = Query(...)):
    """手动触发新闻刷新（需 token 验证）。"""
    if token != REFRESH_TOKEN:
        raise HTTPException(status_code=403, detail="Unauthorized")
    try:
        result = generate_news()
        return {"ok": True, "date": result["date"], "cards": len(result["cards"])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"刷新失败: {e}")


@app.get("/api/health")
def health():
    """健康检查 (nginx upstream)。"""
    return {"status": "ok", "time": datetime.now().isoformat()}


# ═══════════════════════════════════════════════════
#  MAIN (for direct run)
# ═══════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
