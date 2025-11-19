from flask import render_template
from . import bp

@bp.route("/")
def list_sales():
    return render_template("sale/list.html")

@bp.route("/report")
def sales_report():
    return render_template("sale/report.html")
