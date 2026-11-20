
from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from backend.services.auth_service import authenticate_user
from backend.auth.permissions import (
    admin_required,
    organizer_required,
    student_required
)

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email or not password:
        flash("Email and password are required.", "error")
        return redirect(url_for("auth.login_page"))

    user = authenticate_user(email, password)

    if user is None:
        flash("Invalid email or password.", "error")
        return redirect(url_for("auth.login_page"))

    login_user(user)

    return redirect(url_for("auth.dashboard"))


@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login_page"))


@auth.route("/login", methods=["GET"])
def login_page():
    return "SeatLock Login API is ready."


@auth.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    from flask_login import current_user

    return f"Welcome, {current_user.name}! Role: {current_user.role}"

@auth.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    return "Admin access granted"


@auth.route("/organizer/dashboard")
@organizer_required
def organizer_dashboard():
    return "Organizer access granted"


@auth.route("/student/dashboard")
@student_required
def student_dashboard():
    return "Student access granted"