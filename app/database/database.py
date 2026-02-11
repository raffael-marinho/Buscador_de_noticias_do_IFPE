import sqlite3
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

BASE_PATH = os.environ.get("PROJECT_BASE_DIR")
BASE_DIR = os.path.dirname(os.path.abspath(BASE_PATH))
DB_FILE = os.environ.get("DATABASE_FILE")
DB_PATH = os.path.join(BASE_DIR, DB_FILE)

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS noticias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            html_puro TEXT,
            conteudo TEXT,
            campus TEXT,
            url TEXT UNIQUE,
            coletado_em TEXT
        );
    """)

    conn.commit()
    conn.close()

init_db()