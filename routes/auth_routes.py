from flask import Blueprint, render_template, redirect, url_for, request, flash
from models.user_models import is_strong_password, register_user,login_user,session  

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
    
    # Validate form fields
    if not username or not email or not password:
        flash("All fields are required!", "error")
        return redirect(url_for("auth_bp.register_page"))
    
    # Check password strength
    if not is_strong_password(password):
        flash(
            "Your password is weak! It should be at least 9 characters and include "
            "uppercase, lowercase, digits, and symbols.",
            "warning"
        )
        # Stop here: let the user choose a stronger password
        return redirect(url_for("auth_bp.register_page"))
    
    # Register user
    success, _ = register_user(username, email, password)
    
    if success:
        flash("User registered successfully! Please login.", "success")
        return redirect(url_for("auth_bp.login"))
    else:
        flash("Registration failed! Email may already be used.", "error")
        return redirect(url_for("auth_bp.register_page"))

# Login Page (GET)
@auth_bp.route("/login", methods=['GET'])
def login():
    """
    Render the login page.
    """
    return render_template("login.html")
# Login Action (POST)
@auth_bp.route("/login", methods=['POST'])
def login_action():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        
        
        user = login_user(email, password)
        if user:
            session['email'] = user['email']
            session['username'] = user['username']
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password", "error")
            return redirect(url_for("auth_bp.login"))
        
    return  render_template("login.html")


# Dashboard Page (GET)
@auth_bp.route("/dashboard")
def dashboard():
    if "email" not in session:
        return redirect(url_for("auth_bp.login"))
    return render_template("dashboard.html", username=session.get("username"))  

# Logout Action
@auth_bp.route("/logout")
def logout():
    """
    Handle user logout.
    """
    session.pop("email", None)
    session.pop("username", None)
    flash("You have been logged out successfully.", "info")
    return redirect(url_for("auth_bp.login"))