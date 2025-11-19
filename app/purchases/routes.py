from flask import render_template
from . import bp

@bp.route("/")
def list_purchases():
    return render_template("purchase/list.html")
