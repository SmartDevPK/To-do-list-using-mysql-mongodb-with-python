from flask import Blueprint, request, jsonify
from models.user_models import register_user  # Ensure the file is user_model.py

# Create Blueprint
auth_bp = Blueprint("auth_bp", __name__)

# -------------------------------
# Register Route
# -------------------------------
@auth_bp.route("/register", methods=['POST'])
def register():
    data = request.json  # json is a property, no parentheses
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400
    
    # Call model function to register user
    register_user(username, email, password)
    return jsonify({"message": "User registered successfully!"}), 201

# -------------------------------
# Login Route (optional)
# -------------------------------
# from models.user_model import login_user
#
# @auth_bp.route("/login", methods=["POST"])
# def login():
#     data = request.json
#     email = data.get("email")
#     password = data.get("password")
#     
#     if not email or not password:
#         return jsonify({"error": "Email and password are required"}), 400
#     
#     user = login_user(email, password)
#     if user:
#         return jsonify({"message": "Login successful!", "user": user})
#     else:
#         return jsonify({"message": "Invalid email or password"}), 401
