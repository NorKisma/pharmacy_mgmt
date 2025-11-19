from flask import render_template
from . import bp

@bp.route("/")
def list_medicines():
    return render_template("medicine/list.html")
