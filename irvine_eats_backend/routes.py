from flask import request, jsonify, Blueprint
from pathlib import Path
import sqlite3
import csv

DB_PATH = Path("irvine_eats.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row #enables dict-like row access
    return conn

#users
USERS_BP = Blueprint("users", __name__, url_prefix="/users")

@USERS_BP.route("/add", methods=["POST"])
def add_user():
    'Adds a new user to the database'
    data = request.json
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
    'Returns all users in the database'
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return jsonify([dict(u) for u in users])

#restaurants
RESTAURANTS_BP = Blueprint("restaurants", __name__, url_prefix="/restaurants")

@RESTAURANTS_BP.route("/add", methods=["POST"])
def add_restaurant():
    'Adds a new restaurant to the database'
    data = request.json
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO users (name, address, category, phone, url) VALUES (?, ?, ?, ?, ?)",
        (data["name"], data["address"], data["category"], data["phone"], data["url"])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "restaurant added!"}), 201

@RESTAURANTS_BP.route("/api/restaurants", methods=["GET"])
def get_restaurant():
    'Returns all restaurants in the database'
    conn = get_db_connection()
    restaurants = conn.execute("SELECT * FROM restaurants").fetchall()
    conn.close()
    return jsonify([dict(r) for r in restaurants])

#menu
MENU_BP = Blueprint("menu", __name__, url_prefix="/menu")

@MENU_BP.route("/add", methods=["POST"])
def add_menu():
    'Adds a new menu item to the database'
    data = request.json
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO menu (item_name, description, price) VALUES (?, ?, ?)",
        (data["item_name"], data["description"], data["price"])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "menu item added!"}), 201

@MENU_BP.route("/api/menu", methods=["GET"])
def get_menu():
    'Returns all menu items in the database'
    conn = get_db_connection()
    menu_items = conn.execute("SELECT * FROM menu").fetchall()
    conn.close()
    return jsonify([dict(m) for m in menu_items])

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
