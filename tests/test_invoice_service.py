from src.invoice_service import (
    register_invoice,
    is_duplicate_invoice_no,
)


class MockSheet:

    def __init__(self):
        self.rows = []

    def col_values(self, column):
        return self.rows

    def append_row(self, row):
        self.rows.append(row)


class ErrorMockSheet:

    def col_values(self, column):
        return []

    def append_row(self, row):
        raise Exception("登録エラー")


def create_invoice(invoice_no="2607-01"):

    return {
        "請求書No": invoice_no,
        "送付日": "2026/07/17",
        "支払期限": "2026/08/31",
        "取引先": "ミヤシタ技研",
        "案件名": "HP更新",
        "金額": 50000,
        "入金日": "",
    }


def test_register_invoice_success():

    sheet = MockSheet()

    invoice = create_invoice()

    result = register_invoice(sheet, invoice)

    assert result is True
    assert len(sheet.rows) == 1


def test_register_invoice_duplicate():

    sheet = MockSheet()

    sheet.rows = [
        "請求書No",
        "2607-01"
    ]

    invoice = create_invoice()

    result = register_invoice(sheet, invoice)

    assert result is False


def test_register_invoice_no_empty():

    sheet = MockSheet()

    invoice = create_invoice("")

    result = register_invoice(sheet, invoice)

    assert result is False


def test_register_invoice_error():

    sheet = ErrorMockSheet()

    invoice = create_invoice()

    result = register_invoice(sheet, invoice)

    assert result is False