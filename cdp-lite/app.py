import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from modules.importfiles import import_files
from modules.processdata import process_data
from modules.rmfanalysis import rmf_analysis
from modules.openreport import open_report
from modules.viewlogs import view_logs

if __name__ == '__main__':
    app = ttk.Window(title="CDP-Lite", themename="cosmo", resizable=(False, False))
    app.geometry("400x300")

    ttk.Label(app, text="Data management panel", font=("Arial", 14, "bold")).pack(pady=15)
    ttk.Button(app, text="📁 Import data", command=import_files, width=25, bootstyle=PRIMARY).pack(pady=5)
    ttk.Button(app, text="⚙️ Process data", command=process_data, width=25, bootstyle=PRIMARY).pack(pady=5)
    ttk.Button(app, text="🧮 RFM Analysis", command=rmf_analysis, width=25, bootstyle=PRIMARY).pack(pady=5)
    ttk.Button(app, text="📊 Open Power BI report", command=open_report, width=25, bootstyle=SUCCESS).pack(pady=5)
    ttk.Button(app, text="📄 Processing history", command=view_logs, width=25, bootstyle=INFO).pack(pady=5)

    app.mainloop()