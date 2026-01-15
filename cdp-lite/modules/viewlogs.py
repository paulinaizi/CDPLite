from tkinter import messagebox
import os
from .config import LOGS_PATH


def view_logs():
    if os.path.exists(LOGS_PATH):
        os.startfile(LOGS_PATH)
    else:
        messagebox.showinfo("Log info", "Log file not found.")