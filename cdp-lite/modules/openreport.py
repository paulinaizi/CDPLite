import os
from tkinter import messagebox
from .config import REPORT_DIR

def open_report():
    pbix_path = os.path.join(REPORT_DIR, "report.pbix")
    if os.path.exists(pbix_path):
        os.startfile(pbix_path)
    else:
        messagebox.showwarning("File missing", "Power BI report file not found.")