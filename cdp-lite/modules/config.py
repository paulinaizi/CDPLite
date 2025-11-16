import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STAGING_DIR = os.path.join(PROJECT_DIR, "staging")
PROCESSED_DIR = os.path.join(PROJECT_DIR, "processed")
RFM_ANALYSIS_DIR = os.path.join(PROJECT_DIR, "rfm_analysis")
REPORT_DIR = os.path.join(PROJECT_DIR, "report")
LOGS_DIR = os.path.join(PROJECT_DIR, "logs")
LOGS_PATH = os.path.join(LOGS_DIR, "log.txt")

def init_dirs():
    for folder in [STAGING_DIR, PROCESSED_DIR, RFM_ANALYSIS_DIR, REPORT_DIR, LOGS_DIR]:
        os.makedirs(folder, exist_ok=True)