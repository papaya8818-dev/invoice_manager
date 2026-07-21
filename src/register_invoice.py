from pathlib import Path
import argparse
from configparser import ConfigParser

import gspread
from gspread.exceptions import SpreadsheetNotFound
from google.oauth2.service_account import Credentials

from src.logger import logger


# =========================
# 設定
# =========================

# Google Sheets APIのスコープ
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

# プロジェクトフォルダ
BASE_DIR = Path(__file__).resolve().parent.parent

# 設定ファイル
CONFIG_PATH = BASE_DIR / "config" / "config.ini"

def load_config():
    """設定ファイル読み込み"""

    config = ConfigParser()

    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            "設定ファイルが見つかりません"
        )

    config.read(CONFIG_PATH, encoding="utf-8")

    return config


def get_settings():
    """設定値取得"""

    config = load_config()

    spreadsheet_id = config["google"]["spreadsheet_id"]

    return spreadsheet_id

def get_invoice_file(file_path):
    """
    指定された請求書ファイルを取得する
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            "指定した請求書ファイルが見つかりません"
        )

    return file_path


def parse_args():
    """コマンドライン引数解析"""

    parser = argparse.ArgumentParser(
        description="請求書登録処理"
    )

    parser.add_argument(
        "file",
        help="登録する請求書ファイル"
    )

    return parser.parse_args()


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

def is_duplicate_invoice_no(sheet, invoice_no):
    """請求書Noの重複チェック"""
    
    # 請求書No列を取得（1行目の見出しを除外）
    invoice_nos = sheet.col_values(1)[1:]

    # 文字列として比較し、既存データに存在する場合はTrueを返す
    return str(invoice_no) in invoice_nos   


def register_invoice(sheet, invoice):
    """Googleスプレッドシートへ登録"""
  
    invoice_no = invoice["請求書No"]

    if not invoice_no:
        logger.warning("請求書Noが未入力です")
        return False
    
    if is_duplicate_invoice_no(sheet, invoice_no):
        logger.warning(f"登録済みの請求書Noです: {invoice_no}")
        return False

    row = [
        invoice["請求書No"],
        invoice["送付日"],
        invoice["支払期限"],
        invoice["取引先"],
        invoice["案件名"],
        invoice["金額"],
        invoice["入金日"],
    ]

    try:
        sheet.append_row(row)

    except Exception as e:
        logger.exception(f"登録エラー: {e}")
        return False

    return True

def main():

    logger.info("Python処理開始")

    try:
        spreadsheet_id = get_settings()

        args = parse_args()

        file_path = get_invoice_file(args.file)

    except Exception as e:
        logger.error(f"初期処理エラー: {e}")
        return

    spreadsheet = authenticate(spreadsheet_id)

    if spreadsheet is None:
        return
    
    sheet = spreadsheet.sheet1


    invoice = read_invoice_from_excel(file_path)

    if invoice is None:
        return

    result = register_invoice(sheet, invoice)

    if result:
        logger.info("請求データを登録しました！")
    else:
        logger.info(f"請求データの登録を中止しました。請求書No:{invoice['請求書No']}")

if __name__ == "__main__":
    main()
    