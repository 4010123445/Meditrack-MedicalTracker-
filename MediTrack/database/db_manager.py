import sqlite3
from pathlib import Path


DB_FILE = Path(__file__).resolve().parent.parent / "meditrack.db"


class DatabaseManager:
    def __init__(self):
        self.db_path = DB_FILE
        self._init_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        conn = self._get_conn()
        cur = conn.cursor()

        # Patients
        cur.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            contact TEXT
        )
        """)

        # Add contact column if it doesn't exist (migration)
        try:
            cur.execute("ALTER TABLE patients ADD COLUMN contact TEXT")
            conn.commit()
        except sqlite3.OperationalError:
            pass  # Column already exists
        # Medications
        cur.execute("""
        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            name TEXT,
            dosage TEXT,
            frequency TEXT,
            start_date TEXT,
            end_date TEXT,
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        )
        """)

        # Add start_date and end_date columns if they don't exist (migration)
        try:
            cur.execute("ALTER TABLE medications ADD COLUMN start_date TEXT")
            conn.commit()
        except sqlite3.OperationalError:
            pass  # Column already exists
        try:
            cur.execute("ALTER TABLE medications ADD COLUMN end_date TEXT")
            conn.commit()
        except sqlite3.OperationalError:
            pass  # Column already exists

        # Appointments
        cur.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            doctor_name TEXT,
            appointment_date TEXT,
            location TEXT,
            notes TEXT,
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        )
        """)

        # Add notes column if it doesn't exist (migration)
        try:
            cur.execute("ALTER TABLE appointments ADD COLUMN notes TEXT")
            conn.commit()
        except sqlite3.OperationalError:
            pass  # Column already exists

        # Reminders
        cur.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            type TEXT,
            message TEXT,
            trigger_time TEXT,
            is_sent INTEGER DEFAULT 0,
            sent_at TEXT
        )
        """)

        conn.commit()
        conn.close()

    def execute(self, query, params=None):
        query = query.replace("%s", "?")
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(query, params or ())
        conn.commit()
        conn.close()

    def fetch_all(self, query, params=None):
        query = query.replace("%s", "?")
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(query, params or ())
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        conn.close()
        return [dict(zip(columns, row)) for row in rows]


