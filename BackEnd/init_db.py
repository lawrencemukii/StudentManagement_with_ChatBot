import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("students.db")

connection = sqlite3.connect(DB_PATH)
try:
    connection.execute("""CREATE TABLE IF NOT EXISTS students 
                        (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            course TEXT NOT NULL,
                            age INTEGER NOT NULL
                        )
                      """)
    connection.commit()
finally:
    connection.close()