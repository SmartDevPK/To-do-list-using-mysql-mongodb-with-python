from flask import Blueprint, render_template, redirect, url_for, request, flash
from models.user_models import register_user  # Ensure the file is user_models.py

# Create Blueprint
auth_bp = Blueprint("auth_bp", __name__)

# Register Page (GET)
@auth_bp.route("/register", methods=['GET'])
def register_page():
    """
    Render the registration page.
    """
    return render_template("register.html")


# -------------------------------
# Register Action (POST)
# -------------------------------
@auth_bp.route("/register", methods=['POST'])
def register_action():
    """
    Handle registration form submission.
    """
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    
    if not username or not email or not password:
        flash("All fields are required!", "error")
        return redirect(url_for("login.html"))
    
    # Call model function to register user
    register_user(username, email, password)
    
    flash("User registered successfully!", "success")
    return redirect(url_for("login.html"))  # Or redirect to login page


# -------------------------------
# Optional Login Route
# -------------------------------
# from models.user_models import login_user
#
# @auth_bp.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         email = request.form.get("email")
#         password = request.form.get("password")
#         
#         if not email or not password:
#             flash("Email and password are required", "error")
#             return redirect(url_for("auth_bp.login"))
#         
#         user = login_user(email, password)
#         if user:
#             flash("Login successful!", "success")
#             return redirect(url_for("dashboard"))  # Replace with your dashboard route
#         else:
#             flash("Invalid email or password", "error")
#             return redirect(url_for("auth_bp.login"))
#     
#     return render_template("login.html")
