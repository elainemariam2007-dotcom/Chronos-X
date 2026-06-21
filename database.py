import sqlite3

DB_NAME = "database/chronos.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():

    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        priority TEXT,
        deadline TEXT,
        status TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS productivity(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        score INTEGER
    )
    """)

    conn.commit()
    conn.close()