from pathlib import Path
import argparse

from src.excel_reader import read_invoice_from_excel
from src.logger import logger
from src.sheets_client import authenticate
from src.config import get_settings
from src.invoice_service import register_invoice


# =========================
# 設定
# =========================

# Google Sheets APIのスコープ
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

# プロジェクトフォルダ
BASE_DIR = Path(__file__).resolve().parent.parent


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
    