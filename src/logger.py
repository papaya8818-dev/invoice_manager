from pathlib import Path
import logging

# プロジェクトフォルダ
BASE_DIR = Path(__file__).resolve().parent.parent

# ログフォルダ
LOG_DIR = BASE_DIR / "logs"

# ログフォルダ作成
LOG_DIR.mkdir(exist_ok=True)

# ログ設定
logging.basicConfig(
    filename=LOG_DIR / "invoice_manager.log",
    level=logging.INFO,
    encoding="utf-8",
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)