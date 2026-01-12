from tkinter import messagebox
import os
import pandas as pd
import mysql.connector
from datetime import datetime

from .config import RFM_ANALYSIS_DIR, LOGS_PATH
from .processdata import get_db_connection
from .logger import log_message


def fetch_data():
    conn = get_db_connection()
    query = """
        SELECT c.id, c.email, t.amount, t.date
        FROM customers c
        JOIN transactions t ON c.id = t.customer_id;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def calculate_rfm(df: pd.DataFrame) -> pd.DataFrame:
    df["date"] = pd.to_datetime(df["date"])

    snapshot_date = df["date"].max() + pd.Timedelta(days=1)

    rfm = df.groupby("email").agg({
        "date": lambda x: (snapshot_date - x.max()).days,
        "id": "count",
        "amount": "sum"
    })

    rfm.columns = ["recency", "frequency", "monetary"]
    return rfm


def save_rfm_results(rfm: pd.DataFrame):
    os.makedirs(RFM_ANALYSIS_DIR, exist_ok=True)
    output_path = os.path.join(RFM_ANALYSIS_DIR, "rfm_results.csv")
    rfm.to_csv(output_path)
    log_message(f"Saved RFM results to {output_path}")


def rfm_analysis():
    try:
        df = fetch_data()
        if df.empty:
            log_message("No data available for RFM analysis.")
            return

        rfm = calculate_rfm(df)
        save_rfm_results(rfm)
        log_message("RFM analysis completed successfully.")

    except Exception as e:
        log_message(f"Error during RFM analysis: {e}")
