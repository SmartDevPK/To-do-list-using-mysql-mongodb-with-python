from flask import Flask
from routes.auth_routes import auth_bp  # Make sure your file is named auth_routes.py

# -------------------------------
# Create Flask Application
# -------------------------------
app = Flask(__name__)

# -------------------------------
# Register Blueprints / Routes
# -------------------------------
app.register_blueprint(auth_bp)

# -------------------------------
# Run the App
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
