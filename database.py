import os
import sqlite3
from typing import Optional

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.environ.get("MYSQL_PORT", "3306"))
MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "health_prediction_db")

USE_SQLITE = os.environ.get("USE_SQLITE_FALLBACK", "false").lower() == "true"


def _is_test(db_path):
    return db_path == ":memory:" or USE_SQLITE


def _sqlite_conn(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def _mysql_conn():
    import mysql.connector
    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        autocommit=False,
    )


def _to_dict(cursor, row):
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))


def init_db(db_path=""):
    if _is_test(db_path):
        conn = _sqlite_conn(db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                date_of_birth TEXT NOT NULL,
                email TEXT NOT NULL,
                glucose REAL NOT NULL,
                haemoglobin REAL NOT NULL,
                cholesterol REAL NOT NULL,
                remarks TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
        return

    conn = _mysql_conn()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(255) NOT NULL,
            date_of_birth DATE NOT NULL,
            email VARCHAR(255) NOT NULL,
            glucose FLOAT NOT NULL,
            haemoglobin FLOAT NOT NULL,
            cholesterol FLOAT NOT NULL,
            remarks TEXT,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    conn.commit()
    cursor.close()
    conn.close()


def create_patient(full_name, date_of_birth, email, glucose, haemoglobin, cholesterol, remarks="", db_path=""):
    if _is_test(db_path):
        conn = _sqlite_conn(db_path)
        cur = conn.execute(
            "INSERT INTO patients (full_name, date_of_birth, email, glucose, haemoglobin, cholesterol, remarks) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (full_name, date_of_birth, email, glucose, haemoglobin, cholesterol, remarks)
        )
        conn.commit()
        row_id = cur.lastrowid
        conn.close()
        return row_id

    conn = _mysql_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO patients (full_name, date_of_birth, email, glucose, haemoglobin, cholesterol, remarks) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (full_name, date_of_birth, email, glucose, haemoglobin, cholesterol, remarks)
    )
    conn.commit()
    row_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return row_id


def get_all_patients(db_path=""):
    if _is_test(db_path):
        conn = _sqlite_conn(db_path)
        rows = conn.execute("SELECT * FROM patients ORDER BY id").fetchall()
        conn.close()
        return [dict(r) for r in rows]

    conn = _mysql_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients ORDER BY id")
    rows = cursor.fetchall()
    result = [_to_dict(cursor, r) for r in rows]
    cursor.close()
    conn.close()
    return result


def get_patient_by_id(patient_id, db_path="") -> Optional[dict]:
    if _is_test(db_path):
        conn = _sqlite_conn(db_path)
        row = conn.execute("SELECT * FROM patients WHERE id = ?", (patient_id,)).fetchone()
        conn.close()
        return dict(row) if row else None

    conn = _mysql_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
    row = cursor.fetchone()
    result = _to_dict(cursor, row) if row else None
    cursor.close()
    conn.close()
    return result


def get_patient_count(db_path=""):
    if _is_test(db_path):
        conn = _sqlite_conn(db_path)
        result = conn.execute("SELECT COUNT(*) FROM patients").fetchone()
        conn.close()
        return result[0]

    conn = _mysql_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM patients")
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count


def get_recent_patients(limit=5, db_path=""):
    if _is_test(db_path):
        conn = _sqlite_conn(db_path)
        rows = conn.execute("SELECT * FROM patients ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    conn = _mysql_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients ORDER BY id DESC LIMIT %s", (limit,))
    rows = cursor.fetchall()
    result = [_to_dict(cursor, r) for r in rows]
    cursor.close()
    conn.close()
    return result


def update_patient(patient_id, full_name, date_of_birth, email, glucose, haemoglobin, cholesterol, db_path=""):
    if _is_test(db_path):
        conn = _sqlite_conn(db_path)
        conn.execute(
            "UPDATE patients SET full_name=?, date_of_birth=?, email=?, glucose=?, haemoglobin=?, cholesterol=? WHERE id=?",
            (full_name, date_of_birth, email, glucose, haemoglobin, cholesterol, patient_id)
        )
        conn.commit()
        conn.close()
        return

    conn = _mysql_conn()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE patients SET full_name=%s, date_of_birth=%s, email=%s, glucose=%s, haemoglobin=%s, cholesterol=%s WHERE id=%s",
        (full_name, date_of_birth, email, glucose, haemoglobin, cholesterol, patient_id)
    )
    conn.commit()
    cursor.close()
    conn.close()


def update_patient_remarks(patient_id, remarks, db_path=""):
    if _is_test(db_path):
        conn = _sqlite_conn(db_path)
        conn.execute("UPDATE patients SET remarks=? WHERE id=?", (remarks, patient_id))
        conn.commit()
        conn.close()
        return

    conn = _mysql_conn()
    cursor = conn.cursor()
    cursor.execute("UPDATE patients SET remarks=%s WHERE id=%s", (remarks, patient_id))
    conn.commit()
    cursor.close()
    conn.close()


def delete_patient(patient_id, db_path=""):
    if _is_test(db_path):
        conn = _sqlite_conn(db_path)
        conn.execute("DELETE FROM patients WHERE id=?", (patient_id,))
        conn.commit()
        conn.close()
        return

    conn = _mysql_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients WHERE id=%s", (patient_id,))
    conn.commit()
    cursor.close()
    conn.close()


def search_patients(term, db_path=""):
    if not term:
        return get_all_patients(db_path=db_path)

    if _is_test(db_path):
        term_lower = term.lower()
        return [
            r for r in get_all_patients(db_path=db_path)
            if term_lower in r["full_name"].lower() or term_lower in r["email"].lower()
        ]

    conn = _mysql_conn()
    cursor = conn.cursor()
    like = f"%{term}%"
    cursor.execute("SELECT * FROM patients WHERE full_name LIKE %s OR email LIKE %s ORDER BY id", (like, like))
    rows = cursor.fetchall()
    result = [_to_dict(cursor, r) for r in rows]
    cursor.close()
    conn.close()
    return result
