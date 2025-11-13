from tkinter import filedialog, messagebox
import os
import shutil
from datetime import datetime

def copy_with_timestamp(src, dest):
    file_name = os.path.basename(src)
    name, ext = os.path.splitext(file_name)
    timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
    new_name = f"{name}_{timestamp}{ext}"
    dest_path = os.path.join(dest, new_name)
    shutil.copy2(src, dest_path)

def import_files():
    staging_dir = os.path.join(os.path.dirname(__file__), "..", "staging")
    os.makedirs(staging_dir, exist_ok=True)
    files = filedialog.askopenfilenames(title="Select data files", filetypes=[("CSV and JSON Files", "*.csv *.json"), ("CSV Files", "*.csv"), ("JSON Files", "*.json")])
    if files:
        for file in files:
            copy_with_timestamp(file, staging_dir)
        messagebox.showinfo("Import complete", f"{len(files)} files added.")