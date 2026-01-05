import os
import sys
import subprocess
from datetime import datetime
from tkinter import messagebox

from .config import REPORT_DIR, LOGS_PATH


def log_message(message: str) -> None:
    os.makedirs(os.path.dirname(LOGS_PATH), exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOGS_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {message}\n")


def open_report():
    pbix_path = os.path.join(REPORT_DIR, "report.pbix")

    if not os.path.exists(pbix_path):
        messagebox.showwarning(
            "File missing",
            "Power BI report file not found."
        )
        log_message("Power BI report not found.")
        return

    try:
        if sys.platform.startswith("win"):
            os.startfile(pbix_path)
        elif sys.platform == "darwin":
            subprocess.call(["open", pbix_path])
        else:
            subprocess.call(["xdg-open", pbix_path])

        log_message("Power BI report opened successfully.")

    except Exception as e:
        log_message(f"Failed to open Power BI report: {e}")
        messagebox.showerror(
            "Error",
            "Unable to open Power BI report.\n"
            "Ensure Power BI Desktop is installed."
        )
