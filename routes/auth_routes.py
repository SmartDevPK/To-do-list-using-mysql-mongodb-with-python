import os
from flask import (
    Blueprint, render_template, redirect, url_for,
    request, flash, session, 
)
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from models.user_models import (
    is_strong_password, register_user, login_user, reset_password,tasks_collection,
    get_user_by_email, create_task, get_all_tasks,
    edit_task_by_id, edit_task 
)
from models.Email_sending import sending_welcome_email
from models.send_reset_email import send_reset_email

# ------------------------------
# Blueprint
# ------------------------------
auth_bp = Blueprint("auth_bp", __name__)

# ------------------------------
# Registration Routes
# ------------------------------
@auth_bp.route("/register", methods=['GET'])
def register_page():
    return render_template("register.html")


@auth_bp.route("/register", methods=['POST'])
def register_action():
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

# ------------------------------
# Login & Logout Routes
# ------------------------------
@auth_bp.route("/login", methods=['GET'])
def login():
    return render_template("login.html")


@auth_bp.route("/login", methods=['POST'])
def login_action():
    email = request.form.get("email")
    password = request.form.get("password")

    user = login_user(email, password)
    if user:
        session['email'] = user['email']
        session['username'] = user['username']
        return redirect(url_for("auth_bp.tasks"))
    else:
        flash("Invalid email or password", "error")
        return redirect(url_for("auth_bp.login"))


@auth_bp.route("/logout")
def logout():
    session.pop("email", None)
    session.pop("username", None)
    flash("You have been logged out successfully.", "info")
    return redirect(url_for("auth_bp.login"))

# ------------------------------
# Dashboard Route
# ------------------------------
@auth_bp.route("/dashboard")
def dashboard():
    if "email" not in session:
        return redirect(url_for("auth_bp.login"))
    return render_template("dashboard.html", username=session.get("username"))

# ------------------------------
# Password Reset Routes
# ------------------------------
def generate_reset_token(email):
    secret_key = os.getenv('SECRET_KEY')
    s = URLSafeTimedSerializer(secret_key)
    token = s.dumps(email, salt='password-reset-salt')
    reset_link = url_for('auth_bp.reset_password_route', token=token, _external=True)
    return reset_link


@auth_bp.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get("email")
        if not email:
            flash("Please enter your email.", "warning")
            return redirect(url_for("auth_bp.forgot_password"))

        user = get_user_by_email(email)
        if not user:
            flash("Email not found.", "danger")
            return redirect(url_for("auth_bp.forgot_password"))

        reset_link = generate_reset_token(email)
        if send_reset_email(email, reset_link):
            flash("A reset link has been sent to your email.", "success")
        else:
            flash("Error sending email. Please try again.", "danger")

        return redirect(url_for("auth_bp.forgot_password"))

    return render_template("forgot_password.html")


@auth_bp.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password_route(token):
    secret_key = os.getenv('SECRET_KEY')
    s = URLSafeTimedSerializer(secret_key)

    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except SignatureExpired:
        flash("The reset link has expired. Please request a new one.", "warning")
        return redirect(url_for("auth_bp.forgot_password"))
    except BadSignature:
        flash("Invalid reset link.", "danger")
        return redirect(url_for("auth_bp.forgot_password"))

    if request.method == 'POST':
        new_password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not new_password or not confirm_password:
            flash("Please fill out all fields.", "warning")
            return redirect(url_for("auth_bp.reset_password_route", token=token))

        if new_password != confirm_password:
            flash("Passwords do not match.", "warning")
            return redirect(url_for("auth_bp.reset_password_route", token=token))

        success = reset_password(email, new_password)
        if success:
            flash("Your password has been reset successfully. Please login.", "success")
            return redirect(url_for("auth_bp.login"))
        else:
            flash("Error resetting password. Please try again.", "danger")
            return redirect(url_for("auth_bp.reset_password_route", token=token))

    return render_template("reset_password.html", token=token)

# ------------------------------
# Task Routes
# ------------------------------
@auth_bp.route("/tasks", methods=['GET', 'POST'])
def tasks():
    if "email" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("auth_bp.login"))

    if request.method == 'POST':
        title = request.form.get("title")
        description = request.form.get("description")
        status = request.form.get("status", "pending")

        if not title or not description:
            flash("Title and description are required.", "warning")
        else:
            task_id = create_task(title, description, status)
            flash(f"Task created successfully with ID: {task_id}", "success")

        return redirect(url_for("auth_bp.tasks"))

    tasks_list = list(tasks_collection.find())
    return render_template("tasks.html", tasks=tasks_list)


@auth_bp.route("/edit_task/<task_id>", methods=["GET"])
def edit_task_form(task_id):
    if "email" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("auth_bp.login"))

    task = edit_task_by_id(task_id)
    if not task:
        flash("Task not found.", "error")
        return redirect(url_for("auth_bp.tasks"))

    return render_template("edit_task.html", task=task)


# POST route: handle edit form submission
@auth_bp.route("/edit_task/<task_id>", methods=["POST"])
def edit_task_submit(task_id):
    if "email" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("auth_bp.login"))

    title = request.form.get("title")
    description = request.form.get("description")
    status = request.form.get("status", "pending")

    if not title or not description:
        flash("Title and description are required.", "warning")
        return redirect(url_for("auth_bp.edit_task_form", task_id=task_id))

    success = edit_task(task_id, title, description, status)
    if success:
        flash("Task updated successfully.", "success")
    else:
        flash("Failed to update task. Try again.", "danger")

    return redirect(url_for("auth_bp.tasks"))
