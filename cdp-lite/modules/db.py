import mysql.connector

from .config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
from .logger import log_message


def get_db_connection():
    try:
        return mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
        )
    except Exception as e:
        log_message(f"Failed to connect to database: {e}")
        return None

