import sqlite3

DB_PATH = "noticias.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS noticias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            conteudo TEXT,
            campus TEXT,
            url TEXT UNIQUE
        );
    """)

    conn.commit()
    conn.close()
