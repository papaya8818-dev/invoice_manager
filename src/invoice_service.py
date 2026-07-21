from src.logger import logger

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
