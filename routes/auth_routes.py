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


# Register Action (POST)
@auth_bp.route("/register", methods=['POST'])
def register_action():
    """
    Handle registration form submission.
    """
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    
    # Validate form
    if not username or not email or not password:
        flash("All fields are required!", "error")
        return redirect(url_for("auth_bp.login"))  
    
    # Call model function to register user
    register_user(username, email, password)
    
    flash("User registered successfully!", "success")
    return redirect(url_for("auth_bp.login"))  


# Login Page (GET)
@auth_bp.route("/login", methods=['GET'])
def login():
    """
    Render the login page.
    """
    return render_template("login.html")
