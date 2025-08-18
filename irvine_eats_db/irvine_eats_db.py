import csv
import sqlite3

# Create a SQLite database and a table for users, then populate it with data from a CSV file.

conn = sqlite3.connect('irvine_eats.db')
cursor = conn.cursor()

# Create users table.
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    id TEXT NOT NULL,
    pw TEXT NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL
)
''')

# Create restaurants table.
cursor.execute('''
CREATE TABLE IF NOT EXISTS restaurants (
    restaurant_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    hours TEXT NOT NULL,
    category TEXT NOT NULL,
    phone TEXT NOT NULL
)    
''')

# Create menu table.
cursor.execute('''
CREATE TABLE IF NOT EXISTS menu (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_id INTEGER NOT NULL,
    item_name TEXT NOT NULL,
    description TEXT,
    price REAL,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id) ON DELETE CASCADE
)
''')

# Create review table.
cursor.execute('''
CREATE TABLE IF NOT EXISTS reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    restaurant_id INTEGER NOT NULL,
    rating INTEGER CHECK(rating >= 1 AND rating <= 5), 
    comment TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id) ON DELETE CASCADE
)
''')

# add rating from review 
# use this for the average rating for the restaurant 
cursor.execute("""
SELECT restaurants.name, AVG(reviews.rating) AS avg_rating 
FROM restaurants
LEFT JOIN reviews ON restaurants.restaurant_id = reviews.restaurant_id 
GROUP BY restaurants.restaurant_id
""")

# Read data from CSV files and insert into the database.

with open('irvine_eats_user.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cursor.execute('''
            INSERT INTO users (id, pw, email, name) 
            VALUES (?, ?, ?, ?)
        ''', (row['id'], row['pw'], row['email'], row['name']))

with open('irvine_eats_restaurant.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cursor.execute('''
            INSERT INTO restaurants (name, address, hours, category, phone) 
            VALUES (?, ?, ?, ?, ?)
        ''', (row['name'], row['address'], row['hours'], row['category'], row['phone']))

with open('irvine_eats_menu.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cursor.execute('''
            INSERT INTO menu (restaurant_id, item_name, description, price) 
            VALUES (?, ?, ?, ?)
        ''', (row['restaurant_id'], row['item_name'], row.get('description'), row.get('price')))

with open('irvine_eats_review.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cursor.execute('''
            INSERT INTO reviews (user_id, restaurant_id, rating, comment) 
            VALUES (?, ?, ?, ?)
        ''', (row['user_id'], row['restaurant_id'], row['rating'], row.get('comment')))

conn.commit()
cursor.close()
