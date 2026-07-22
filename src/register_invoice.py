from pathlib import Path
import argparse

from src.logger import logger
from src.config import get_settings
from src.excel_reader import read_invoice_from_excel
from src.sheets_client import authenticate
from src.invoice_service import register_invoice


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


def process_invoice(file_path):
    """
    請求書登録処理
    """

    spreadsheet_id = get_settings()

    spreadsheet = authenticate(spreadsheet_id)

    if spreadsheet is None:
        return "ERROR"

    sheet = spreadsheet.sheet1

    invoice = read_invoice_from_excel(file_path)

    if invoice is None:
        return "ERROR"

    result = register_invoice(sheet, invoice)

    return result



def main():

    try:
        args = parse_args()

        file_path = get_invoice_file(args.file)

        result = process_invoice(file_path)

        if result == "SUCCESS":
            logger.info("処理正常終了")
            return 0
        
        elif result == "DUPLICATE":
            return 2
        
        else:
            logger.error("処理失敗")
            return 1

    except Exception as e:
        logger.exception(f"処理エラー: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
    