from flask import request, jsonify, Blueprint
from pathlib import Path
import sqlite3
<<<<<<< HEAD
import csv
=======
import requests
import os
import time
>>>>>>> 8c900057994d3ce41f899c8971876b441fec2da4

PLACES_KEY = os.getenv("google_api")
LOCATION = "33.6846,-117.8265"
RADIUS = 5000
BASE = "https://maps.googleapis.com/maps/api/place"
NEARBY = f"{BASE}/nearbysearch/json"
DETAILS = f"{BASE}/details/json"
DB_PATH = Path("irvine_eats.db")

url = (
    f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    f"?location={LOCATION}&radius={RADIUS}&type=restaurant&key={PLACES_KEY}"
)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row #enables dict-like row access
    return conn

def fetch_nearby(latlng: str, radius: int = RADIUS):
    params = {
        "location": latlng,
        "radius": radius,
        "type": "restaurant",
        "key": PLACES_KEY
    }
    while True:
        r = requests.get(NEARBY, params=params, timeout=5)
        r.raise_for_status()
        payload = r.json()
        for item in payload.get("results", []):
            yield item
        nxt = payload.get("next_page_token")
        if not nxt: break
        time.sleep(2) # Google requiers a short wait before using the next_page_token
        params = {"pagetoken": nxt, "key": PLACES_KEY}

def fetch_details(place_id: str):
    fields = "name,formatted_address,types,formatted_phone_number,website,url"
    params = {"place_id": place_id, "fields": fields, "key": PLACES_KEY}
    r = requests.get(DETAILS, params=params, timeout=5)
    r.raise_for_status()
    return r.json().get("result", {})

#users
USERS_BP = Blueprint("users", __name__, url_prefix="/users")

@USERS_BP.route("/add", methods=["POST"])
def add_user():
    data = request.get_json()
    'Adds a new user to the database'
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO users (id, pw, name, email) VALUES (?, ?, ?, ?)",
        (data["id"], data["pw"], data["name"], data["email"])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "user added!"}), 201

@USERS_BP.route("/api/users", methods=["GET"])
def get_user():
    'Returns users in the database'
    user_id = request.args.get("id") # e.g., /api/users?id=1
    conn = get_db_connection()
    if user_id is None: # Return all users if no id is provided
        users = conn.execute("SELECT * FROM users").fetchall()
    else:
        users = conn.execute("SELECT * FROM users where id = ?", (user_id,)).fetchall()
    conn.close()
    return jsonify([dict(u) for u in users])

#restaurants
RESTAURANTS_BP = Blueprint("restaurants", __name__, url_prefix="/restaurants")

@RESTAURANTS_BP.route("/add", methods=["POST"])
def add_restaurant():
    conn = get_db_connection()
    cur = conn.cursor()
    inserted = 0

    for hit in fetch_nearby(LOCATION, RADIUS):
        place_id = hit.get["place_id"]
        if not place_id:
            continue
        det = fetch_details(place_id)

        name = det.get("name") or hit.get("name")
        address = det.get("formatted_address")
        phone = det.get("formatted_phone_number")
        url = det.get("website") or det.get("url")

        types = det.get("types", []) or hit.get("types", [])
        category = next((t for t in types if t not in {"point_of_interest","establishment","food","restaurant"}), "restaurant")

        cur.execute(
            "INSERT INTO restaurants (name, address, phone, category, url, place_id) VALUES (?, ?, ?, ?, ?, ?)",
            (name, address, phone, category, url, place_id)
        )
        inserted += 1
    
    conn.commit()
    conn.close()
    return jsonify({"message": f"{inserted} restaurants added!"}), 201

@RESTAURANTS_BP.route("/api/restaurants", methods=["GET"])
def get_restaurant():
    'Returns restaurants in the database'
    rest_id = request.args.get("restaurant_id")
    conn = get_db_connection()
    if rest_id is None:
        restaurants = conn.execute("SELECT * FROM restaurants").fetchall()
    else:
        restaurants = conn.execute("SELECT * FROM restaurants where restaurant_id = ?", (rest_id,)).fetchall()
    conn.close()
    return jsonify([dict(r) for r in restaurants])

#menu
MENU_BP = Blueprint("menu", __name__, url_prefix="/menu")

@MENU_BP.route("/add", methods=["POST"])
def add_menu():
    'Adds a new menu item to the database'
    response = requests.get(url)
    data = response.json()
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO menu (restaurant_id, item_name, description, price) VALUES (?, ?, ?, ?)",
        (data["restaurant_id"], data["item_name"], data["description"], data["price"])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "menu item added!"}), 201

@MENU_BP.route("/api/menu", methods=["GET"])
def get_menu():
    'Returns menu items in the database'
    item_id = request.args.get("item_id")
    conn = get_db_connection()
    if item_id is None:
        menu_items = conn.execute("SELECT * FROM menu").fetchall()
    else:
        menu_items = conn.execute("SELECT * FROM menu where item_id = ?", (item_id,)).fetchall()
    conn.close()
    return jsonify([dict(m) for m in menu_items])

<<<<<<< HEAD
#account authorization (logging in, signing up)
AUTH_BP = Blueprint("auth", __name__, url_prefix="/auth")

@AUTH_BP.route("/login", methods=["POST"])
def login():
    'Logs the user in if login info is verified'
    data = request.json
    username = data.get("id")
    password = data.get("pw")
    usercsv = "../irvine_eats_db/irvine_eats_user.csv"

    if is_valid_login(username, password, usercsv):
        return jsonify({"message": "Login successful"}), 200
    
    return jsonify({"error": "Invalid username or password"}), 401

def is_valid_login(username, password, csvfile):
    'Checks if username and password are valid'
    with open(csvfile, newline="") as usercsv:
        user_info = csv.DictReader(usercsv)
        
        for row in user_info:
            if (row["id"] == username and row["pw"] == password):
                return True
        
        return False
=======
#review
REVIEW_BP = Blueprint("review", __name__, url_prefix="/review")

@REVIEW_BP.route("/add", methods=["POST"])
def add_review():
    'Adds a new review to the database'
    data = request.get_json()
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO reviews (user_id, restaurant_id, rating, comment) VALUES (?, ?, ?, ?)",
        (data["user_id"], data["restaurant_id"], data["rating"], data["comment"])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "review item added!"}), 201

@MENU_BP.route("/api/reviews", methods=["GET"])
def get_review():
    'Returns reviews in the database'
    review_id = request.get_json()
    conn = get_db_connection()
    if review_id is None:
        reviews = conn.execute("SELECT * FROM reviews").fetchall()
    else:
        reviews = conn.execute("SELECT * FROM reviews where review_id = ?", (review_id,)).fetchall()
    conn.close()

    return jsonify([dict(r) for r in reviews])
>>>>>>> 8c900057994d3ce41f899c8971876b441fec2da4
