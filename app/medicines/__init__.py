from flask import Blueprint

bp = Blueprint("medicine_bp", __name__, template_folder="templates")

from . import routes
