from tkinter import filedialog, messagebox
import os
import shutil
from datetime import datetime
from .config import STAGING_DIR

def copy_with_timestamp(src, dest):
    file_name = os.path.basename(src)
    name, ext = os.path.splitext(file_name)
    timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
    new_name = f"{name}_{timestamp}{ext}"
    dest_path = os.path.join(dest, new_name)
    shutil.copy2(src, dest_path)

def import_files():
    files = filedialog.askopenfilenames(title="Select data files", filetypes=[("CSV and JSON Files", "*.csv *.json"), ("CSV Files", "*.csv"), ("JSON Files", "*.json")])
    if files:
        for file in files:
            copy_with_timestamp(file, STAGING_DIR)
        messagebox.showinfo("Import complete", f"{len(files)} files added.")