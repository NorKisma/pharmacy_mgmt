# app/auth/routes.py

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from urllib.parse import urlparse, urljoin

from . import bp  # auth blueprint
from ..models import User
from ..extensions import db
from .forms import LoginForm, RegisterForm
from ..utils import log_action  # optional audit logging

# ----------------------------
# Safe URL check for "next"
# ----------------------------
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


# ----------------------------
# Login route
# ----------------------------
@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            log_action("User logged in", object_type="User", object_id=user.id)
            flash("Logged in successfully.", "success")

            next_page = request.args.get("next")
            if not next_page or not is_safe_url(next_page):
                next_page = url_for("main.dashboard")
            return redirect(next_page)

        flash("Invalid email or password.", "danger")

    elif form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", "danger")

    return render_template("auth/login.html", form=form)


# ----------------------------
# Logout route
# ----------------------------
@bp.route("/logout")
@login_required
def logout():
    log_action("User logged out", object_type="User", object_id=current_user.id)
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("auth.login"))


# ----------------------------
# Register route
# ----------------------------
@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "warning")
            return redirect(url_for("auth.register"))

        user = User(email=email, password_hash=generate_password_hash(form.password.data))
        try:
            db.session.add(user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash("An error occurred. Please try again.", "danger")
            return redirect(url_for("auth.register"))

        log_action("User registered", object_type="User", object_id=user.id)
        flash("Account created successfully. You can now log in.", "success")
        return redirect(url_for("auth.login"))

    elif form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", "danger")

    return render_template("auth/register.html", form=form)


# ----------------------------
# List Users route
# ----------------------------
@bp.route('/users')
@login_required
def list_users():
    users = User.query.all()  # fetch all users
    return render_template('auth/list_users.html', users=users)
