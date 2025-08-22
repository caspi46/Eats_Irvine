import sqlite3

conn = sqlite3.connect('irvine_eats.db')

cursor = conn.cursor()
cursor.execute("SELECT * FROM restaurants")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()