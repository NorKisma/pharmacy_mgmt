# app/auth/routes.py

from flask import render_template, redirect, url_for, flash, request, abort, jsonify,current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from urllib.parse import urlparse, urljoin
from functools import wraps

from . import bp
from ..models import User
from ..extensions import db, limiter
from .forms import LoginForm, RegisterForm
from ..utils import log_action,log_action

# ----------------------------------
# Role-based access decorator
# ----------------------------------
def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ----------------------------------
# Safe URL check for "next"
# ----------------------------------
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

# ----------------------------------
# LOGIN
# ----------------------------------

@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        user = User.query.filter_by(email=email).first()
        current_app.logger.info(f"Login attempt: {email}, User found: {bool(user)}")

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Logged in successfully.", "success")
            next_page = request.args.get("next")
            if not next_page or not is_safe_url(next_page):
                next_page = url_for("main.dashboard")
            return redirect(next_page)

        flash("Invalid email or password.", "danger")
        current_app.logger.warning(f"Login failed for email: {email}")

    return render_template("auth/login.html", form=form)
# ----------------------------------
# LOGOUT
# ----------------------------------
@bp.route("/logout")
@login_required
def logout():
    log_action("User logged out", object_type="User", object_id=current_user.id)
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("auth.login"))

# ----------------------------------
# REGISTER (Admin Only)
# ----------------------------------
@bp.route("/register", methods=["GET", "POST"])
#@login_required
@role_required("admin")
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "warning")
            return redirect(url_for("auth.register"))

        user = User(
            name=form.name.data,
            email=email,
            password_hash=generate_password_hash(form.password.data),
            role=form.role.data or "staff"
        )

        try:
            db.session.add(user)
            db.session.commit()
            log_action("User registered", object_type="User", object_id=user.id)
        except Exception:
            db.session.rollback()
            flash("An error occurred. Please try again.", "danger")
            return redirect(url_for("auth.register"))

        flash("Account created successfully.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)

# ----------------------------------
# USER MANAGEMENT (Admin Only)
# ----------------------------------
@bp.route("/users")
#@login_required
@role_required("admin")
def list_users():
    page = request.args.get('page', 1, type=int)
    users_pagination = User.query.paginate(page=page, per_page=10)
    return render_template("users.html", users_pagination=users_pagination)

@bp.route("/user/add", methods=["GET", "POST"])
#@login_required
@role_required("admin")
def add_user():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email").lower()
        password = request.form.get("password")
        role = request.form.get("role") or "staff"

        if User.query.filter_by(email=email).first():
            flash("Email already exists.", "warning")
            return redirect(url_for("auth.add_user"))

        user = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
            role=role
        )
        try:
            db.session.add(user)
            db.session.commit()
            log_action("User added", object_type="User", object_id=user.id)
            flash("User added successfully!", "success")
            return redirect(url_for("auth.list_users"))
        except Exception:
            db.session.rollback()
            flash("Failed to add user.", "danger")
            return redirect(url_for("auth.add_user"))

    return render_template("add_user.html")

@bp.route("/user/delete/<int:id>", methods=["POST"])
@login_required
@role_required("admin")
def delete_user(id):
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        log_action("User deleted", object_type="User", object_id=id)
        return jsonify({"status":"success","message":"User deleted successfully"})
    except Exception:
        db.session.rollback()
        return jsonify({"status":"error","message":"Failed to delete user"}), 500

# ----------------------------------
# CHANGE PASSWORD
# ----------------------------------
@bp.route('/change-password', methods=["GET", "POST"])
@login_required
@limiter.limit("5 per 15 minutes")
def change_password():
    if request.method == "POST":
        current_pwd = request.form.get("current_password")
        new_pwd = request.form.get("new_password")
        confirm_pwd = request.form.get("confirm_password")

        if not check_password_hash(current_user.password_hash, current_pwd):
            flash("Current password is incorrect.", "danger")
        elif new_pwd != confirm_pwd:
            flash("New passwords do not match.", "danger")
        else:
            current_user.password_hash = generate_password_hash(new_pwd)
            db.session.commit()
            log_action("User changed password", object_type="User", object_id=current_user.id)
            flash("Password updated successfully.", "success")
            return redirect(url_for("main.dashboard"))

    return render_template("auth/change_password.html")
