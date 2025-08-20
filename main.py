from flask import Flask, render_template
from routes.auth_routes import auth_bp
from db import get_mysql_connection
import os


# Create Flask Application
app = Flask(__name__)

# set a secret key for session management
app.secret_key = os.urandom(24)

# Register Blueprints / Routes
app.register_blueprint(auth_bp)


# Database Connection Test
conn = get_mysql_connection()
if conn:
    print("Database connected successfully")
    conn.close()   # close after testing
else:
    print("Failed to connect")


# Routes
@app.route("/")
def home():
    return render_template("index.html")


# Run the App
if __name__ == "__main__":
    app.run(debug=True)
