from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from models.user_models import is_strong_password, register_user, login_user, reset_password
from models.send_reset_email import send_reset_email
from itsdangerous import URLSafeTimedSerializer
import os
# -------------------------------
# Create Blueprint
# -------------------------------
auth_bp = Blueprint("auth_bp", __name__)


# -------------------------------
# Register Page (GET)
# -------------------------------
@auth_bp.route("/register", methods=['GET'])
def register_page():
    """Render the registration page."""
    return render_template("register.html")




# -------------------------------
# Register Action (POST)
# -------------------------------
@auth_bp.route("/register", methods=['POST'])
def register_action():
    """Handle registration form submission."""
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    if not username or not email or not password:
        flash("All fields are required!", "error")
        return redirect(url_for("auth_bp.register_page"))

    if not is_strong_password(password):
        flash(
            "Your password is weak! It should be at least 9 characters and include "
            "uppercase, lowercase, digits, and symbols.",
            "warning"
        )
        return redirect(url_for("auth_bp.register_page"))

    success, _ = register_user(username, email, password)
    if success:
        flash("User registered successfully! Please login.", "success")
        return redirect(url_for("auth_bp.login"))
    else:
        flash("Registration failed! Email may already be used.", "error")
        return redirect(url_for("auth_bp.register_page"))


# -------------------------------
# Login Page (GET)
# -------------------------------
@auth_bp.route("/login", methods=['GET'])
def login():
    """Render the login page."""
    return render_template("login.html")


# -------------------------------
# Login Action (POST)
# -------------------------------
@auth_bp.route("/login", methods=['POST'])
def login_action():
    """Handle login form submission."""
    email = request.form.get("email")
    password = request.form.get("password")

    user = login_user(email, password)
    if user:
        session['email'] = user['email']
        session['username'] = user['username']
        return redirect(url_for("auth_bp.dashboard"))  # Ensure this route exists
    else:
        flash("Invalid email or password", "error")
        return redirect(url_for("auth_bp.login"))


# -------------------------------
# Dashboard Page (GET)
# -------------------------------
@auth_bp.route("/dashboard")
def dashboard():
    """Render dashboard page for logged-in users."""
    if "email" not in session:
        return redirect(url_for("auth_bp.login"))
    return render_template("dashboard.html", username=session.get("username"))


# -------------------------------
# Logout Action
# -------------------------------
@auth_bp.route("/logout")
def logout():
    """Handle user logout."""
    session.pop("email", None)
    session.pop("username", None)
    flash("You have been logged out successfully.", "info")
    return redirect(url_for("auth_bp.login"))



#generate rest token
def generate_reset_token(email):
    """
    Generate a secure password reset link for a given email.
    """
    secret_key = os.getenv('SECRET_KEY')  # Load your secret key from .env
    s = URLSafeTimedSerializer(secret_key)
    token = s.dumps(email, salt='password-reset-salt')
    reset_link = url_for('auth_bp.reset_password_route', token=token, _external=True)
    return reset_link


# -------------------------------
# Forgot / Reset Password Route
# -------------------------------
@auth_bp.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password():
    """
    Render the forgot password page and handle reset link requests.
    """
    if request.method == 'POST':
        email = request.form.get("email")

        if not email:
            flash("Please enter your email.", "warning")
            return redirect(url_for("auth_bp.forgot_password"))
        
        # Generate reset link
        reset_link = generate_reset_token(email)

        # Send reset link via email
        if send_reset_email(email, reset_link):
            flash("A reset link has been sent to your email.", "success")
        else:
            flash("Email not found or error sending email.", "danger")

        return redirect(url_for("auth_bp.forgot_password"))

    # GET request – render the forgot password form
    return render_template("forgot_password.html")
    
   
    

    # GET request
    return render_template("forgot_password.html")
