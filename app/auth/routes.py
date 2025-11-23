from flask import render_template, redirect, url_for, flash, request, abort, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from urllib.parse import urlparse, urljoin
from functools import wraps

# Import from your application structure
from . import bp
from .forms import LoginForm, RegisterForm, ChangePasswordForm
from ..models import User, Role
from ..extensions import db, limiter
from ..utils import log_action

# ----------------------------------
# CONSTANTS
# ----------------------------------
DEFAULT_HASH_SCHEME = "pbkdf2:sha256"

# ----------------------------------
# HELPER FUNCTIONS
# ----------------------------------

def is_safe_url(target):
    """
    Checks if a target URL is safe to redirect to, preventing open redirect vulnerabilities.
    """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc

def verify_and_upgrade_password(user, password: str) -> bool:
    """
    Verify the password for the user. Automatically upgrade old hashes
    to the default modern scheme if needed.
    """
    # Ensure your User model has a 'password_hash' field, or change this to 'password'
    stored_hash = user.password_hash 

    if check_password_hash(stored_hash, password):
        # Upgrade hash if it's not the default scheme
        if not stored_hash.startswith(DEFAULT_HASH_SCHEME):
            user.password_hash = generate_password_hash(password, method=DEFAULT_HASH_SCHEME)
            db.session.commit()
        return True

    return False

# ----------------------------------
# DECORATORS
# ----------------------------------

def role_required(*roles):
    """
    Restricts access to a route to users who possess one of the specified roles.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()
            
            # Check if the user has a role and if it matches the requirements
            if not current_user.role or current_user.role.name not in roles:
                flash("You do not have permission to access this resource.", "danger")
                return abort(403)

            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ----------------------------------
# ROUTES
# ----------------------------------

@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user and verify_and_upgrade_password(user, password):
            login_user(user)
            flash("Logged in successfully.", "success")
            
            # Handle the "next" argument securely
            next_page = request.args.get('next')
            if not next_page or not is_safe_url(next_page):
                next_page = url_for('main.dashboard')
            
            return redirect(next_page)
        else:
            current_app.logger.warning(f"Login failed for: {email}")
            flash("Invalid email or password.", "danger")

    return render_template("auth/login.html", form=form)



@bp.route("/logout")
@login_required
def logout():
    user_id = current_user.id
    try:
        logout_user()
        log_action("User logged out", object_type="User", object_id=user_id)
        flash("Logged out successfully.", "info")
    except Exception as e:
        current_app.logger.error(f"Logout error for user {user_id}: {e}")
        flash("An error occurred while logging out.", "danger")

    return redirect(url_for("auth.login"))

@bp.route("/register", methods=["GET", "POST"])
#@login_required
#@role_required("admin") 
def register():
    # 1. Safety: Redirect if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = RegisterForm()

    if form.validate_on_submit():
        # 2. Extract Data
        name = form.name.data.strip()
        email = form.email.data.strip().lower()
        password = form.password.data

        # 3. Check for duplicates (Email)
        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "warning")
            return render_template("auth/register.html", form=form)
        
        # 4. Check for duplicates (Name - Optional, only if names must be unique)
        # if User.query.filter_by(name=name).first():
        #     flash("This name is already taken.", "warning")
        #     return render_template("auth/register.html", form=form)

        # 5. Fetch Default Role (Crucial Step)
        # We assume your Role table has a row where name='user' (or 'staff')
        default_role = Role.query.filter_by(name="user").first()
        
        if not default_role:
            # Fallback for safety to prevent crashing if DB is empty
            flash("System Error: Default role not configured.", "danger")
            return render_template("auth/register.html", form=form)

        # 6. Create User
        new_user = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password, method=DEFAULT_HASH_SCHEME),
            role_id=default_role.id  # Backend automatically assigns this
        )
        
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)









from flask_wtf import FlaskForm

class DummyForm(FlaskForm):
    pass

@bp.route("/users")
@login_required
#@role_required("admin")
def list_users():
    page = request.args.get("page", 1, type=int)
    users_pagination = User.query.paginate(page=page, per_page=10)
    form = DummyForm()
    return render_template("auth/users.html", users_pagination=users_pagination, csrf_form=form)


@bp.route("/user/delete/<int:id>", methods=["POST"]) 
@login_required
@role_required("admin")
def delete_user(id):
    if current_user.id == id:
        return jsonify({"status": "error", "message": "You cannot delete your own account."}), 400
        
    user = User.query.get_or_404(id)
    
    # Soft delete is usually safer, but your code implemented hard delete.
    # If you want soft delete: user.is_deleted = True; user.deleted_at = datetime.utcnow()
    db.session.delete(user) 
    db.session.commit()
    
    log_action("User hard deleted", object_type="User", object_id=id)
    return jsonify({"status": "success", "message": "User deleted successfully"})

@bp.route("/change-password", methods=["GET", "POST"])
@login_required
@limiter.limit("5 per 15 minutes")
def change_password():
    form = ChangePasswordForm()

    if current_user.is_deleted:
        flash("Your account is deactivated. Contact admin.", "danger")
        return redirect(url_for("main.dashboard"))
        
    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data

        if not current_user.check_password(current_password):
            flash("Current password is incorrect.", "danger")
            return render_template("auth/change_password.html", form=form)

        if current_user.check_password(new_password):
            flash("New password cannot be the same as the current password.", "warning")
            return render_template("auth/change_password.html", form=form)

        current_user.set_password(new_password)
        db.session.commit()
        log_action("User changed password", object_type="User", object_id=current_user.id)

        # Keep user logged in after password change
        login_user(current_user, fresh=True) 

        flash("Password updated successfully.", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("auth/change_password.html", form=form)