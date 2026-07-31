#!/bin/bash
# ═══════════════════════════════════════════════════
#  PSU Daily News — Ubuntu 22.04 部署脚本
# ═══════════════════════════════════════════════════
# 使用方法:
#   1. 把 server/ 目录拷贝到服务器: scp -r server/ user@your-server:/opt/psu-news/
#   2. 编辑下面的 DOMAIN 和 DEEPSEEK_API_KEY
#   3. chmod +x deploy.sh && sudo ./deploy.sh
# ═══════════════════════════════════════════════════

set -e

# ═══════════ 修改这里 ═══════════
DOMAIN="your-domain.com"                          # 你的域名（小程序必须要 HTTPS 域名）
DEEPSEEK_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxx" # DeepSeek API Key
REFRESH_TOKEN="psu-daily-refresh-2026"            # 手动刷新用的 token（改一个你自己的）
# ════════════════════════════════

APP_DIR="/opt/psu-news"
VENV_DIR="$APP_DIR/venv"
USER="${SUDO_USER:-root}"

echo "================================================"
echo "  PSU Daily News — Ubuntu 部署"
echo "  Domain: $DOMAIN"
echo "================================================"

# ── 1. 系统依赖 ──
echo "[1/6] 安装系统依赖..."
apt-get update -qq
apt-get install -y -qq python3 python3-venv python3-pip nginx certbot python3-certbot-nginx cron

# ── 2. Python 虚拟环境 ──
echo "[2/6] 创建 Python 虚拟环境..."
mkdir -p "$APP_DIR"
cp -r ./* "$APP_DIR/"
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"
pip install --upgrade pip -q
pip install -r "$APP_DIR/requirements.txt" -q
echo "  ✓ Python 环境就绪"

# ── 3. 环境变量 ──
echo "[3/6] 配置环境变量..."
cat > "$APP_DIR/env.sh" << ENVEOF
export DEEPSEEK_API_KEY="$DEEPSEEK_API_KEY"
export REFRESH_TOKEN="$REFRESH_TOKEN"
ENVEOF
chmod 600 "$APP_DIR/env.sh"
echo "  ✓ env.sh 已创建"

# ── 4. systemd 服务 ──
echo "[4/6] 配置 systemd 服务..."
cat > /etc/systemd/system/psu-news-api.service << UNITEOF
[Unit]
Description=PSU Daily News API
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$APP_DIR
EnvironmentFile=$APP_DIR/env.sh
ExecStart=$VENV_DIR/bin/uvicorn main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
UNITEOF

systemctl daemon-reload
systemctl enable psu-news-api
systemctl restart psu-news-api
echo "  ✓ systemd 服务已启动"

# ── 5. Nginx ──
echo "[5/6] 配置 Nginx 反向代理..."
cat > /etc/nginx/sites-available/psu-news << NGINXEOF
server {
    listen 80;
    server_name $DOMAIN;

    # 小程序 API
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 120s;
    }

    # 健康检查
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
    }
}
NGINXEOF

ln -sf /etc/nginx/sites-available/psu-news /etc/nginx/sites-enabled/
# 删掉默认站点（避免冲突）
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx
echo "  ✓ Nginx 配置完成 (HTTP)"

# ── 6. HTTPS 证书 (Let's Encrypt) ──
echo "[6/6] 申请 HTTPS 证书..."
# 注意：域名必须已解析到本机 IP，且 80 端口可公网访问
certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos --email "admin@$DOMAIN" --redirect || echo "  ⚠ SSL 证书申请失败，请手动执行: sudo certbot --nginx -d $DOMAIN"

# ── 7. Crontab 每日定时刷新 ──
echo ""
echo "配置 crontab 每日定时刷新..."
CRON_JOB="0 8 * * * source $APP_DIR/env.sh && cd $APP_DIR && $VENV_DIR/bin/python news_engine.py >> $APP_DIR/cron.log 2>&1"
(crontab -l 2>/dev/null | grep -v "psu-news" ; echo "$CRON_JOB") | crontab -
echo "  ✓ Crontab: 每天 08:00 (UTC) → 美东凌晨 04:00"

# ── Done ──
echo ""
echo "================================================"
echo "  ✅ 部署完成！"
echo ""
echo "  验证: curl https://$DOMAIN/api/news/today"
echo "  日志: journalctl -u psu-news-api -f"
echo "  Cron: crontab -l"
echo ""
echo "  ⚠ 小程序要求: 在微信公众平台 → 开发管理 →"
echo "    服务器域名 → request合法域名 中添加:"
echo "    https://$DOMAIN"
echo "================================================"
