import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "tasks.db")

def db_connect():
	conn = sqlite3.connect("tasks.db")
	conn.row_factory = sqlite3.Row
	return conn

def init_db():
	conn = db_connect()
	cursor = conn.cursor()

	cursor.execute("""
		CREATE TABLE IF NOT EXISTS tasks (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			title TEXT NOT NULL,
			status TEXT NOT NULL
		)
	""")

	conn.commit()
	conn.close()

init_db()