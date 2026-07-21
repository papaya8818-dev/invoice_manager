from pathlib import Path

import pytest

from src.config import load_config, get_settings


def test_load_config(tmp_path, monkeypatch):

    config_file = tmp_path / "config.ini"

    config_file.write_text(
        """
[google]
spreadsheet_id=test_id
""",
        encoding="utf-8"
    )

    monkeypatch.setattr(
        "src.config.CONFIG_PATH",
        config_file
    )

    config = load_config()

    assert config["google"]["spreadsheet_id"] == "test_id"


def test_load_config_file_not_found(tmp_path, monkeypatch):

    config_file = tmp_path / "not_found.ini"

    monkeypatch.setattr(
        "src.config.CONFIG_PATH",
        config_file
    )

    with pytest.raises(FileNotFoundError):
        load_config()


def test_get_settings(tmp_path, monkeypatch):

    config_file = tmp_path / "config.ini"

    config_file.write_text(
        """
[google]
spreadsheet_id=test_id
""",
        encoding="utf-8"
    )

    monkeypatch.setattr(
        "src.config.CONFIG_PATH",
        config_file
    )

    result = get_settings()

    assert result == "test_id"