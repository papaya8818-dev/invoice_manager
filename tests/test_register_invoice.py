from datetime import datetime

from src.register_invoice import format_invoice_no
from src.register_invoice import is_duplicate_invoice_no


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