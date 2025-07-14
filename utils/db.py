import sqlite3
import pandas as pd
from datetime import datetime

# Persistent database file (it will stay in Streamlit cloud workspace)
DB_FILE = "logs.db"

conn = sqlite3.connect(DB_FILE, check_same_thread=False)

def create_table():
    conn.execute("""
        CREATE TABLE IF NOT EXISTS logs_definitions (
            event_id TEXT PRIMARY KEY,
            name TEXT,
            description TEXT,
            category TEXT,
            module TEXT,
            severity TEXT,
            version INTEGER,
            created_by TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    """)
    conn.commit()

create_table()

def insert_log(name, description, category, module, severity, version, created_by):
    now = datetime.utcnow().isoformat()
    event_id = f"{name}_{version}_{now}"
    conn.execute("""
        INSERT INTO logs_definitions
        (event_id, name, description, category, module, severity, version, created_by, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (event_id, name, description, category, module, severity, version, created_by, now, now))
    conn.commit()

def fetch_logs(q=None, category=None):
    query = "SELECT * FROM logs_definitions WHERE 1=1"
    params = []

    if q:
        query += " AND (name LIKE ? OR description LIKE ?)"
        params.extend([f"%{q}%", f"%{q}%"])

    if category:
        query += " AND category = ?"
        params.append(category)

    df = pd.read_sql_query(query, conn, params=params)
    return df

def fetch_versions(name):
    query = "SELECT version, created_by, created_at FROM logs_definitions WHERE name = ? ORDER BY version DESC"
    df = pd.read_sql_query(query, conn, params=(name,))
    return df

def delete_all_logs():
    conn.execute("DELETE FROM logs_definitions")
    conn.commit()
