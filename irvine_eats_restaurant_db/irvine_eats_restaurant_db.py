import sqlite3, csv

conn = sqlite3.connect("irvine_eats_restaruant.db")
cur = conn.cursor()
cur.execute("PRAGMA foreign_keys = ON;")

# ---- import irvine_eats_restaruant.csv ----
with open("irvine_eats_restaurant.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = [
        (
            int(r["restaurant_id"]),
            r["name"],
            r.get("address"),
            float(r["rating"]) if r.get("rating") else None,
        )
        for r in reader
    ]
cur.executemany(
    "INSERT OR REPLACE INTO restaurants (restaurant_id, name, address, rating) VALUES (?,?,?,?)",
    rows,
)

# ---- import irvine_eats_menu.csv ----
with open("irvine_eats_menu.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = [
        (
            int(r["item_id"]),
            int(r["restaurant_id"]),
            r["item_name"],
            r.get("category"),
            r.get("description"),
            float(r["price"]) if r.get("price") else None,
        )
        for r in reader
    ]
cur.executemany(
    """INSERT OR REPLACE INTO menu
       (item_id, restaurant_id, item_name, category, description, price)
       VALUES (?,?,?,?,?,?)""",
    rows,
)

conn.commit()
conn.close()



