from flask import Blueprint, render_template, session, redirect, request, url_for, flash
from flask_login import login_required, current_user
from ..decorators import role_required, permission_required
from ..utils import log_action

# --------------------------
# Blueprint
# --------------------------
bp = Blueprint("main", __name__, template_folder='templates')

# --------------------------
# Dashboard
# --------------------------
@bp.route('/')
def dashboard():
    if current_user.is_authenticated:
        if current_user.role == "admin":
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('staff.dashboard'))
    else:
        return redirect(url_for('auth.login'))




# --------------------------
# Settings (Admin only with permission)
# --------------------------
@bp.route('/settings')
@login_required
@permission_required('update_settings')
def settings():
    """
    Admin-only settings page.
    """
    log_action("Accessed settings page")
    return render_template("main/settings.html", user=current_user)


# --------------------------
# Language Selector
# --------------------------
@bp.route("/set_language/<lang_code>")
def set_language(lang_code):
    """
    Update session language and redirect back to previous page.
    """
    if lang_code in ['en', 'so', 'ar']:
        session['lang'] = lang_code
        flash(f"Language changed to {lang_code.upper()}", "success")
    return redirect(request.referrer or url_for('main.dashboard'))
