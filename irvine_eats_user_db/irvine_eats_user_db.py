import csv
import sqlite3

# Create a SQLite database and a table for users, then populate it with data from a CSV file.

conn = sqlite3.connect('irvine_eats_user.db')
cursor = conn.cursor()

# user_id is set to AUTOINCREMENT to ensure unique IDs for each user.
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    id TEXT NOT NULL,
    pw TEXT NOT NULL,
    email TEXT NOT NULL
)
''')

with open('irvine_eats_users.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cursor.execute('''
            INSERT INTO users (id, pw, email) 
            VALUES (?, ?, ?)
        ''', (row['id'], row['pw'], row['email']))

conn.commit()
cursor.close()
