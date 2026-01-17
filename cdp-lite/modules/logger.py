from datetime import datetime
from .config import LOGS_PATH


def log_message(message: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOGS_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {message}\n")
