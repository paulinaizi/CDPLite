from tkinter import messagebox
import os
from .config import LOGS_PATH

def view_logs():
    if os.path.exists(LOGS_PATH):
        os.startfile(LOGS_PATH)
    else:
        messagebox.showwarning("File missing", "Log file not found.")