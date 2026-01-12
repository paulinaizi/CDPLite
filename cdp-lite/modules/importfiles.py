from tkinter import filedialog, messagebox
import os
import shutil
from datetime import datetime
from .config import STAGING_DIR
from .logger import log_message


def copy_with_timestamp(src, dest):
    file_name = os.path.basename(src)
    name, ext = os.path.splitext(file_name)
    timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
    new_name = f"{name}_{timestamp}{ext}"
    dest_path = os.path.join(dest, new_name)
    shutil.copy2(src, dest_path)


def import_files():
    files = filedialog.askopenfilenames(title="Select data files",
                                        filetypes=[("CSV and JSON Files", "*.csv *.json"),
                                                   ("CSV Files", "*.csv"),
                                                   ("JSON Files", "*.json")
                                                   ])

    if not files:
        return

    success_count = 0

    for file in files:
        try:
            copy_with_timestamp(file, STAGING_DIR)
            success_count += 1
        except Exception as e:
            log_message(f"Failed to import file {os.path.basename(file)}: {e}")

    if success_count > 0:
        log_message(f"Imported {success_count} files to staging directory.")

    if success_count == len(files):
        messagebox.showinfo("Import info", f"Imported {success_count} files successfully.")
    elif success_count == 0:
        messagebox.showwarning("Import info", "Failed to import all files.")
    else:
        messagebox.showinfo("Import info", f"Imported {success_count}/{len(files)} files. Some files failed.")
