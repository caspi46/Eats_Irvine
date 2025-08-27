from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pathlib import Path
import csv, threading
from datetime import datetime

app = Flask(__name__)
CORS(app)

CSV_PATH = Path("irvine_eats_user.csv")
CSV_FIELDS = ["user_id", "id", "pw", "name", "email"]
_lock = threading.Lock()

def ensure_csv_has_header():
    """Create the CSV file with a header row if missing."""
    if not CSV_PATH.exists:
        with open(CSV_PATH, mode='w', newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()

@app.route("/api/users", methods=["POST"])
def save_user():
    '''
    Save user data into CSV file.

    Expects json like:
    {
        "id": "ojh1234",
        "pw": "1547",
        "name": "Alice"
    }
    '''
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400
    
    row = {
        "id": str(data.get("id", "")).strip(),
        "pw": str(data.get("pw", "")).strip(),
        "name": str(data.get("name", "")).strip()
    }

    ensure_csv_has_header()
    with _lock: # avoid race conditions if multiple requests arrive
        with open(CSV_PATH, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writerow(row)
    
    return jsonify({"ok": True, "saved": row}), 201

@app.route("/api/users.csv", methods=["GET"])
def download_csv():
    "Download a CSV file from a local server filesystem."
    ensure_csv_has_header()
    return send_file(CSV_PATH, mimetype="text/CSV", as_attachment=True, download_name="irvine_eats_user.csv")

if __name__ == "__main__":
    # pip install flask flask-cors
    # python app.py
    app.run()

    
