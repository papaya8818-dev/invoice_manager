from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials
from openpyxl import load_workbook

# =========================
# 設定
# =========================

# Google Sheets APIのスコープ
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

# プロジェクトフォルダ
BASE_DIR = Path(__file__).resolve().parent.parent

# スプレッドシートID
SPREADSHEET_ID = "1h1iTqcLn7NHWqEc8Ndjge_pCN4kAiKAtboSyqjg3tGs"

# 請求書フォルダ
INVOICE_DIR = BASE_DIR / "invoices"


def authenticate():
    """Google Sheetsへ接続"""

    # 認証ファイル
    credentials_path = BASE_DIR / "credentials.json"

    # 認証
    creds = Credentials.from_service_account_file(
        credentials_path,
        scopes=SCOPES
    )

    gc = gspread.authorize(creds)

    # スプレッドシートを開く
    spreadsheet = gc.open_by_key(SPREADSHEET_ID)

    print("Google Sheetsへ接続できました！")

    return spreadsheet

    
def read_invoice_from_excel(file_path):
    """
    Excel請求書から請求データを読み込む。

    Args:
        file_path (str): 請求書ファイルのパス

    Returns:
        dict: 請求データ
    """

    wb = load_workbook(file_path, data_only=True)
    ws = wb["請求書"]

    invoice = {
        "請求書No": ws["F2"].value,
        "送付日": ws["F3"].value.strftime("%Y/%m/%d"),
        "支払期限": ws["F4"].value.strftime("%Y/%m/%d"),
        "取引先": ws["B3"].value,
        "案件名": ws["B4"].value,
        "金額": int(ws["F31"].value),
        "入金日": ""
    }

    return invoice


def register_invoice(sheet, invoice):
    """Googleスプレッドシートへ登録"""
  
    row = [
        invoice["請求書No"],
        invoice["送付日"],
        invoice["支払期限"],
        invoice["取引先"],
        invoice["案件名"],
        invoice["金額"],
        invoice["入金日"],
    ]

    sheet.append_row(row)

def main():
    spreadsheet = authenticate()
    sheet = spreadsheet.sheet1

    file_path = (
        INVOICE_DIR
        / "2607-02_ミヤシタ技研様_岡山営業所関連_HP更新・新ロゴ.xlsx"
    )

    invoice = read_invoice_from_excel(file_path)

    register_invoice(sheet, invoice)

    print("請求データを登録しました！")

if __name__ == "__main__":
    main()