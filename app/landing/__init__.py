

from flask import Blueprint


from . import routes
from app.landing.routes import landing_bp
app.register_blueprint(landing_bp) # type: ignore
from . import routes