from flask import Blueprint

# supplier/__init__.py
bp = Blueprint("supplier_bp", __name__, template_folder="templates")


from . import routes
