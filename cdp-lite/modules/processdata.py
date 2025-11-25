import os
import shutil
import re
from datetime import datetime
import pandas as pd
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

from .config import STAGING_DIR, PROCESSED_DIR, LOGS_PATH

DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'cdp_user'
DB_PASSWORD = 'cdp_12345'
DB_NAME = "cdp_lite"

LOG_FILE_PATH = LOGS_PATH

def log_message(message: str) -> None:
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {message}\n")

def get_db_connection():
    return mysql.connector.connect(
        host = DB_HOST,
        port = DB_PORT,
        user = DB_USER,
        password = DB_PASSWORD,
        database = DB_NAME
    )

def ensure_tables_exist(conn):
    create_customers = """
    CREATE TABLE IF NOT EXISTS customers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        email VARCHAR(255) UNIQUE,
        phone VARCHAR(50),
        city VARCHAR(100),
        gender VARCHAR(20),
        age INT,
        created_at DATETIME
    );
    """

    create_transactions = """
    CREATE TABLE IF NOT EXISTS transactions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        transaction_id BIGINT UNIQUE,
        customer_id INT,
        amount DECIMAL(10,2),
        date DATETIME,
        product_category VARCHAR(100),
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    );
    """

    cursor = conn.cursor()
    cursor.execute(create_customers)
    cursor.execute(create_transactions)
    conn.commit()
    cursor.close()


def normalize_email(value):
    if pd.isna(value):
        return None
    return str(value).strip().lower()

def normalize_phone(value):
    if pd.isna(value):
        return None
    s = str(value)
    digits = re.sub(r"\D", "", s)
    if digits.startswith("48") and len(digits) > 9:
        digits = digits[2:]
    if len(digits) < 6:
        return None
    return digits

def normalize_city(value):
    if pd.isna(value):
        return None
    s = str(value).strip()
    return s.lower().capitalize()

def normalize_gender(value):
    if pd.isna(value):
        return None
    s = str(value).strip().lower()
    if s in ("f", "female", "k", "kobieta"):
        return "female"
    if s in ("m", "male", "mezczyzna", "mężczyzna"):
        return "male"
    return None

def parse_age_from_raw(value):
    if pd.isna(value):
        return None
    s = str(value)
    m = re.search(r"(\d+)", s)
    if m:
        return int(m.group(1))
    return None

def age_from_birth_year(value):
    if pd.isna(value):
        return None
    try:
        year = int(value)
    except ValueError:
        return None
    current_year = datetime.now().year
    age = current_year - year
    if 0 < age < 120:
        return age
    return None

def to_datetime_safe(series, dayfirst=True):
    return pd.to_datetime(series, errors="coerce", dayfirst=dayfirst)

def unify_customers_from_source_a(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    first_names = []
    last_names = []
    for full in df.get("fullName", []):
        if pd.isna(full):
            first_names.append(None)
            last_names.append(None)
        else:
            parts = str(full).strip().split()
            if len(parts) == 1:
                first_names.append(parts[0].title())
                last_names.append(None)
            else:
                first_names.append(parts[0].title())
                last_names.append(" ".join(parts[1:]).title())

    df["first_name"] = first_names
    df["last_name"] = last_names
    df["email"] = df["mail"].apply(normalize_email) if "mail" in df.columns else None
    df["phone"] = df["phoneNumber"].apply(normalize_phone) if "phoneNumber" in df.columns else None
    df["city_unified"] = df["city"].apply(normalize_city) if "city" in df.columns else None
    df["gender_unified"] = df["gender"].apply(normalize_gender) if "gender" in df.columns else None
    df["age_unified"] = df["age"].apply(parse_age_from_raw) if "age" in df.columns else None
    df["created_at_unified"] = to_datetime_safe(df["createdAt"]) if "createdAt" in df.columns else None

    return pd.DataFrame({
        "first_name": df["first_name_unified"],
        "last_name": df["last_name_unified"],
        "email": df["email_unified"],
        "phone": df["phone_unified"],
        "city": df["city_unified"],
        "gender": df["gender_unified"],
        "age": df["age_unified"],
        "created_at": df["created_at_unified"],
    })

def unify_transactions(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["customer_email_unified"] = df["customer_email"].apply(normalize_email)
    df["date_unified"] = to_datetime_safe(df["date"])
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    return pd.DataFrame({
        "transaction_id": df["transaction_id"],
        "customer_email": df["customer_email_unified"],
        "amount": df["amount"],
        "date": df["date_unified"],
        "product_category": df["product_category"],
    })

def deduplicate_customers(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.sort_values(by=["created_at"], ascending=True)
    df = df.drop_duplicates(subset=["email"], keep="first")
    return df

def upsert_customers(conn, customers_df: pd.DataFrame):
    customers_df = customers_df.copy()
    customers_df = customers_df[~customers_df["email"].isna()]
    if customers_df.empty:
        return
    
    sql = """
    INSERT INTO customers
        (first_name, last_name, email, phone, city, gender, age, created_at)
    VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s)
    ON DUPLICATE KEY UPDATE
        first_name = VALUES(first_name),
        last_name = VALUES(last_name),
        phone = VALUES(phone),
        city = VALUES(city),
        gender = VALUES(gender),
        age = VALUES(age),
        created_at = VALUES(created_at);
    """

    cursor = conn.cursor()
    data = []
    for _, row in customers_df.iterrows():
        data.append((
            row["first_name"],
            row["last_name"],
            row["email"],
            row["phone"],
            row["city"],
            row["gender"],
            int(row["age"]) if not pd.insa(row["age"]) else None,
            row["created_at"].to_pydatetime() if not pd.isna(row["created_at"]) else None,
        ))
    cursor.executemany(sql, data)
    conn.commit()
    cursor.close()

def insert_transactions(conn, transactions_df: pd.DataFrame):
    transactions_df = transactions_df.copy()
    transactions_df = transactions_df[
        (~transactions_df["customer_email"].isna()) &
        (~transactions_df["date"].isna()) &
        (~transactions_df["amount"].isna())
    ]
    if transactions_df.empty:
        return
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, email FROM customers;")
    rows = cursor.fetchall()
    email_to_id = {row["email"].lower(): row["id"] for row in rows}

    transactions_df["customer_id"] = transactions_df["customer_email"].apply(
        lambda e: email_to_id.get(e.lower()) if isinstance(e, str) else None
    )

    transactions_df = transactions_df[~transactions_df["customer_id"].isna()]
    if transactions_df.empty:
        cursor.close()
        return

    sql = """
    INSERT INTO transactions
        (transaction_id, customer_id, amount, date, product_category)
    VALUES
        (%s,%s,%s,%s,%s)
    ON DUPLICATE KEY UPDATE
        customer_id = VALUES(customer_id),
        amount = VALUES(amount),
        date = VALUES(date),
        product_category = VALUES(product_category);
    """

    data = []
    for _, row in transactions_df.iterrows():
        data.append((
            int(row["transaction_id"]),
            int(row["customer_id"]),
            float(row["amount"]),
            row["date"].to_pydatetime() if not pd.isna(row["date"]) else None,
            row["product_category"],
        ))

    cursor.executemany(sql, data)
    conn.commit()
    cursor.close()

def process_data():
    try:
        os.makedirs(STAGING_DIR, exist_ok=True)
        os.makedirs(PROCESSED_DIR, exist_ok=True)

        files = [
            os.path.join(STAGING_DIR, f)
            for f in os.listdir(STAGING_DIR)
            if os.path.isfile(os.path.join(STAGING_DIR, f))
        ]

        if not files:
            messagebox.showinfo("Process data", "Brak plików w katalogu staging.")
            return

        customers_frames = []
        transactions_frames = []
        processed_files = []

        for path in files:
            filename = os.path.basename(path)
            ext = os.path.splitext(filename)[1].lower()

            try:
                if ext == ".json":
                    df = pd.read_json(path)
                elif ext == ".csv":
                    df = pd.read_csv(path)
                else:
                    continue

                cols = [c.lower() for c in df.columns]

                if "transaction_id" in cols or ("amount" in cols and "customer_email" in cols):
                    unified = unify_transactions(df)
                    transactions_frames.append(unified)
                else:
                    if "fullname" in cols or "mail" in cols:
                        unified = unify_customers_from_source_a(df)
                        customers_frames.append(unified)
                    elif "first_name" in cols and "last_name" in cols and "email" in cols:
                        unified = unify_customers_from_source_b(df)
                        customers_frames.append(unified)
                    else:
                        continue

                processed_files.append(path)

            except Exception:
                continue

        if not customers_frames and not transactions_frames:
            messagebox.showinfo("Process data", "Brak poprawnych danych do przetwarzania.")
            return

        try:
            conn = get_db_connection()
        except Exception as e:
            messagebox.showerror(
                "Process data",
                f"Nie udało się połączyć z bazą danych.\nSprawdź Docker / MySQL.\n\n{e}"
            )
            return

        ensure_tables_exist(conn)

        if customers_frames:
            all_customers = pd.concat(customers_frames, ignore_index=True)
            all_customers = deduplicate_customers(all_customers)
            upsert_customers(conn, all_customers)

        if transactions_frames:
            all_transactions = pd.concat(transactions_frames, ignore_index=True)
            insert_transactions(conn, all_transactions)

        conn.close()

        for src in processed_files:
            dst = os.path.join(PROCESSED_DIR, os.path.basename(src))
            try:
                shutil.move(src, dst)
            except Exception:
                pass

        messagebox.showinfo("Process data", "Przetwarzanie danych zakończone pomyślnie.")

    except Exception as e:
        messagebox.showerror("Process data", f"Wystąpił błąd:\n{e}")

   


    
    
