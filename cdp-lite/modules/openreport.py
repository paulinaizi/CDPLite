import os
import sys
import subprocess
from tkinter import messagebox

from .config import REPORT_DIR
from .logger import log_message


def open_report():
    pbix_path = os.path.join(REPORT_DIR, "report.pbix")

    if not os.path.exists(pbix_path):
        messagebox.showwarning(
            "Report warning",
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
            "Report error",
            "Unable to open Power BI report.\n"
            "Ensure Power BI Desktop is installed."
        )
