import sqlite3

def connect_db():
    conn = sqlite3.connect("students.db")
    return conn

def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            course TEXT
        )
    """)

    conn.commit()
    conn.close()