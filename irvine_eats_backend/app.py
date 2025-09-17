from flask import Flask, send_from_directory 
from routes import USERS_BP, RESTAURANTS_BP, MENU_BP

app = Flask(__name__)
app.register_blueprint(USERS_BP)
app.register_blueprint(RESTAURANTS_BP)
app.register_blueprint(MENU_BP)

if __name__ == "__main__":
    app.run(debug=True)
