import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STAGING_DIR = os.path.join(PROJECT_DIR, "staging")
PROCESSED_DIR = os.path.join(PROJECT_DIR, "processed")
RFM_ANALYSIS_DIR = os.path.join(PROJECT_DIR, "rfm_analysis")
REPORT_DIR = os.path.join(PROJECT_DIR, "report")
LOGS_DIR = os.path.join(PROJECT_DIR, "logs")