from flask import Flask, send_from_directory 
from routes import USERS_BP, RESTAURANTS_BP, MENU_BP

app = Flask(__name__, static_folder ="../irvine_eats_frontend/dist", static_url_path="/")
app.register_blueprint(USERS_BP)
app.register_blueprint(RESTAURANTS_BP)
app.register_blueprint(MENU_BP)

def index():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=True) # add argument: port=5000 for connecting frontend 
