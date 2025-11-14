from tkinter import messagebox
import os
from .config import LOGS_DIR

def view_logs():
    logs_path = os.path.join(LOGS_DIR, "log.txt")
    if os.path.exists(logs_path):
        os.startfile(logs_path)
    else:
        messagebox.showwarning("File missing", "Log file not found.")