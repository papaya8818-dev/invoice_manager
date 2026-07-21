from pathlib import Path
from configparser import ConfigParser

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