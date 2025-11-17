from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from . import bp
from ..models import User
from ..extensions import db
from .forms import LoginForm, RegisterForm
from ..utils import log_action  # optional audit logging

@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            log_action("User logged in", object_type="User", object_id=user.id)
            flash("Logged in successfully.", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("main.dashboard"))
        flash("Invalid email or password.", "danger")
    elif form.errors:
        # show form validation errors (CSRF, etc.)
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", "danger")
    return render_template("auth/login.html", form=form)

@bp.route("/logout")
@login_required
def logout():
    log_action("User logged out", object_type="User", object_id=current_user.id)
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("auth.login"))

@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Email already registered.", "warning")
            return redirect(url_for("auth.register"))

        user = User(
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
        log_action("User registered", object_type="User", object_id=user.id)
        flash("Account created successfully. You can now log in.", "success")
        return redirect(url_for("auth.login"))

    elif form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", "danger")

    return render_template("auth/register.html", form=form)
