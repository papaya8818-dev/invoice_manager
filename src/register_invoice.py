from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials

# Google Sheets APIのスコープ
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

# プロジェクトフォルダ
BASE_DIR = Path(__file__).resolve().parent.parent

# 認証ファイル
credentials_path = BASE_DIR / "credentials.json"

# 認証
creds = Credentials.from_service_account_file(
    credentials_path,
    scopes=SCOPES
)

gc = gspread.authorize(creds)

# スプレッドシートを開く
spreadsheet = gc.open_by_key("1h1iTqcLn7NHWqEc8Ndjge_pCN4kAiKAtboSyqjg3tGs")

print("Google Sheetsへ接続できました！")

sheet = spreadsheet.sheet1

invoice = {
    "請求書No": "2608-01",
    "送付日": "2026/07/10",
    "支払期限": "2026/08/10",
    "取引先": "株式会社サンプル",
    "案件名": "ホームページ更新",
    "金額": 15000,
    "入金日": ""
}

row = [
    invoice["請求書No"],
    invoice["送付日"],
    invoice["支払期限"],
    invoice["取引先"],
    invoice["案件名"],
    invoice["金額"],
    invoice["入金日"],
]

sheet.append_row(list(invoice.values()))

print("請求データを登録しました！")
