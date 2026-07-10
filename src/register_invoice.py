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