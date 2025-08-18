from flask import Blueprint,request, jsonify
from models.user_models import register_user

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/register", methods=['PSOT'])
def regsiter():
    data = request.json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    register_user(username, email, password)
    return jsonify({"message": "User registered successfully!"})


# @auth_bp.route("/login", methods=["POST"])
# def login():
#     data = request.json
#     email = data.get("email")
#     password = data.get("password")
    
#     user = login_user(email, password)
#     if user:
#         return jsonify({"message": "Login successful!", "user": user})
#     else:
        # return jsonify({"message": "Invalid email or password"}), 401