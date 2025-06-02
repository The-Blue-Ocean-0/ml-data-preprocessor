import requests
import json


# 設定項目
API_KEY = "AIzaSyAt_3oICwf8exsn_on0UkegTKrIYWOXDqo"
URL_TO_ANALYZE = "https://br-icloud.com.br"  # ← https:// を必ず入れる
STRATEGY = "desktop"
API_ENDPOINT = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

# API呼び出し用パラメータ
params = {
    "url": URL_TO_ANALYZE,
    "strategy": STRATEGY,
    "category": ["performance", "accessibility", "seo"],
    "key": API_KEY
}

# API呼び出し
response = requests.get(API_ENDPOINT, params=params)
data = response.json()

# デバッグ出力（エラー時用）
if "lighthouseResult" not in data:
    print("🚨 APIレスポンスに 'lighthouseResult' が含まれていません。")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    exit()

# スコア取得
performance_score = data["lighthouseResult"]["categories"]["performance"]["score"]
accessibility_score = data["lighthouseResult"]["categories"]["accessibility"]["score"]
seo_score = data["lighthouseResult"]["categories"]["seo"]["score"]

# Core Web Vitals取得
audits = data["lighthouseResult"]["audits"]
lcp = audits["largest-contentful-paint"]["displayValue"]
cls = audits["cumulative-layout-shift"]["displayValue"]
inp = audits.get("interaction-to-next-paint", {}).get("displayValue", "N/A")

# 結果出力
print(f"📄 URL: {URL_TO_ANALYZE}")
print(f"⚡ Performance Score: {performance_score}")
print(f"♿ Accessibility Score: {accessibility_score}")
print(f"🔍 SEO Score: {seo_score}")
print(f"📈 LCP: {lcp}")
print(f"🔄 CLS: {cls}")
print(f"⌛ INP: {inp}")
