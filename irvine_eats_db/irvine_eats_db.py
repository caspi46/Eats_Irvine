import sqlite3, csv

conn = sqlite3.connect("irvine_eats.db")
cur = conn.cursor() 
cur.execute("PRAGMA foreign_keys = ON")


# user 
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY, 
        id TEXT NOT NULL,
        name TEXT NOT NULL, 
        email TEXT UNIQUE, 
        password TEXT NOT NULL
)
""")

# restaurant 
cur.execute("""
CREATE TABLE IF NOT EXISTS restaurants (
        restaurant_id INTEGER PRIMARY KEY, 
        name TEXT NOT NULL, 
        address TEXT NOT NULL
)
""")

# review 
cur.execute("""
CREATE TABLE IF NOT EXISTS reviews (
        review_id INTEGER PRIMARY KEY, 
        user_id INTEGER, 
        restaurant_id INTEGER, 
        rating INTEGER CHECK(rating >= 1 AND rating <= 5), 
        comment TEXT, 
        FOREIGN KEY(user_id) REFERENCES users(user_id), 
        FOREIGN KEY(restaurant_id) REFERENCES restaurants(restaurant_id)
)
""")

# add rating from review 
cur.execute("""
SELECT restaurants.name, AVG(reviews.rating) AS avg_rating 
FROM restaurants
LEFT JOIN reviews ON restaurants.restaurant_id = reviews.restaurant_id 
GROUP BY restaurants.restaurant_id
""")


# sample user data: 
# id = "kyungrk"
# name = "Kenny"
# email = "kenny.com"
# password = "theKennyKim"

# cur.execute("INSERT INTO users (id, name, email, password) VALUES (?,?,?,?)", 
#             (id, name, email, password))

cur.execute("SELECT name FROM sqlite_master WHERE type='table';") 
print(cur.fetchall())

cur.execute("SELECT * FROM users")
print(cur.fetchall())

conn.commit()
conn.close()