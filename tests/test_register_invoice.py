from datetime import datetime

from src.register_invoice import format_invoice_no
from src.register_invoice import is_duplicate_invoice_no
from openpyxl import Workbook

from src.register_invoice import read_invoice_from_excel


class MockSheet:

    def col_values(self, column):
        return [
            "請求書No",
            "2607-01",
            "2607-02",
        ]
    

def test_is_duplicate_invoice_no_true():

    sheet = MockSheet()

    result = is_duplicate_invoice_no(
        sheet,
        "2607-01"
    )

    assert result is True


def test_is_duplicate_invoice_no_false():

    sheet = MockSheet()

    result = is_duplicate_invoice_no(
        sheet,
        "2607-03"
    )

    assert result is False


def test_format_invoice_no_datetime():

    result = format_invoice_no(
        datetime(2026, 7, 15)
    )

    assert result == "2607-15"


def test_format_invoice_no_string():

    result = format_invoice_no(
        "2607-01"
    )

    assert result == "2607-01"


def test_read_invoice_from_excel(tmp_path):

    # テスト用Excel作成
    file_path = tmp_path / "test_invoice.xlsx"

    wb = Workbook()

    ws = wb.active
    ws.title = "請求書"

    ws["F2"] = "2607-01"
    ws["F3"] = datetime(2026, 7, 15)
    ws["F4"] = datetime(2026, 8, 31)
    ws["B3"] = "ミヤシタ技研"
    ws["B4"] = "HP更新"
    ws["F31"] = 50000

    wb.save(file_path)


    # 関数実行
    invoice = read_invoice_from_excel(file_path)


    # 結果確認
    assert invoice["請求書No"] == "2607-01"
    assert invoice["取引先"] == "ミヤシタ技研"
    assert invoice["案件名"] == "HP更新"
    assert invoice["金額"] == 50000