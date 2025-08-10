import sqlite3
import os

# Ensure folder exists
os.makedirs('database', exist_ok=True)

conn = sqlite3.connect('database/app.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mobile TEXT UNIQUE,
    password TEXT,
    hint TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS graphical_passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mobile TEXT,
    app_name TEXT,
    category TEXT,
    password_seq TEXT
)
''')

conn.commit()
conn.close()
print("Database initialized.")
