import sqlite3

conn = sqlite3.connect('voting.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    candidate TEXT
)
''')

conn.commit()
conn.close()

print("Database created successfully!")