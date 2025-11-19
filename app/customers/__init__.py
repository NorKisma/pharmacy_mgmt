from flask import Blueprint

bp = Blueprint("customer_bp", __name__, template_folder="templates")  # <-- note the name
from . import routes
