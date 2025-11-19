from flask import Blueprint, render_template

bp = Blueprint('customer_bp', __name__, url_prefix='/customers')

@bp.route('/')
def list_customers():
    return render_template('customers/list.html')
