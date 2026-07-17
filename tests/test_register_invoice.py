from datetime import datetime

from src.register_invoice import format_invoice_no


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