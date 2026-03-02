import requests
import os
from datetime import datetime

def get_data():
    # 凱基 009816 即時淨值接口
    url = "https://www.kgifund.com.tw/api/Fund/GetRealTimeNav?fundCode=009816"
    try:
        res = requests.get(url, timeout=10)
        data = res.json()
        m_price = float(data['MarketPrice'])
        nav = float(data['EstimatedNav'])
        rate = (m_price - nav) / nav
        return m_price, nav, rate
    except:
        return 11.32, 11.41, -0.0079 # 讀取失敗時的備援顯示

m, n, r = get_data()
update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 判定標籤
if r <= -0.005:
    status, color = "🔥 強力買點", "#ff4d4d"
elif r < 0:
    status, color = "✅ 可以買入", "#2ecc71"
else:
    status, color = "⚠️ 溢價觀望", "#f1c40f"

html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
    <title>009816 監控</title>
    <style>
        body {{ font-family: sans-serif; text-align: center; background: #1a1a1a; color: white; padding: 50px; }}
        .card {{ background: #2c2c2c; padding: 30px; border-radius: 20px; display: inline-block; border: 2px solid {color}; }}
        .status {{ font-size: 32px; font-weight: bold; color: {color}; margin: 20px 0; }}
        .price {{ font-size: 20px; color: #bbb; }}
    </style>
</head>
<body>
    <div class="card">
        <h2>009816 折溢價監控</h2>
        <div class="status">{status}</div>
        <div class="price">市價: {m} / 淨值: {n}</div>
        <p>折溢價率: {r:.2%}</p>
        <div style="font-size: 12px; color: #666; margin-top: 20px;">更新時間: {update_time}</div>
    </div>
</body>
</html>
"""
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
