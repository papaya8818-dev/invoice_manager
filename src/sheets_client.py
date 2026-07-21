from pathlib import Path

import gspread
from gspread.exceptions import SpreadsheetNotFound
from google.oauth2.service_account import Credentials

from src.logger import logger

# プロジェクトフォルダ
BASE_DIR = Path(__file__).resolve().parent.parent


# Google Sheets APIのスコープ
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]


def authenticate(spreadsheet_id):
    """Google Sheetsへ接続"""

    # 認証ファイル
    credentials_path = BASE_DIR / "credentials.json"

    # 認証
    try:
        # 認証ファイル読み込み
        creds = Credentials.from_service_account_file(
            credentials_path,
            scopes=SCOPES
        )

        # Google Sheets API認証
        gc = gspread.authorize(creds)

        # スプレッドシートを開く
        spreadsheet = gc.open_by_key(spreadsheet_id)

        logger.info("Google Sheetsへ接続できました！")

        return spreadsheet

    except FileNotFoundError:
        logger.error("認証ファイルが見つかりません")
        return None

    except SpreadsheetNotFound:
        logger.error("指定したスプレッドシートが見つかりません")
        return None

    except Exception as e:
        logger.exception(f"Google Sheets接続エラー: {e}")
        return None