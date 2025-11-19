from flask import Blueprint

bp = Blueprint("purchase_bp", __name__, template_folder="templates")

from . import routes
