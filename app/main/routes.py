from flask import render_template
from flask_login import login_required, current_user
from . import bp
from ..decorators import permission_required

@bp.route('/')

def dashboard():
    return render_template('main/dashboard.html', user=current_user)

@bp.route('/settings')
@login_required
@permission_required('update_settings')
def settings():
    return "Settings page (Admin only)"
