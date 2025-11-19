from flask import render_template
from . import bp

@bp.route("/")
def list_suppliers():
    return render_template("supplier/list.html")
