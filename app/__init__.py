import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

from .extensions import db, migrate, login_manager, mail, babel, limiter, get_locale
from .config import get_config
from .models import User

# ---------------------------
# User loader for flask-login
# ---------------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"

# ---------------------------
# Create Flask app
# ---------------------------
def create_app(config_name=None):
    app = Flask(__name__, instance_relative_config=False)

    # Load config
    cfg = get_config(os.getenv("FLASK_ENV", "development"))
    app.config.from_object(cfg)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)
    babel.init_app(app, locale_selector=get_locale)  # <-- new 3.x syntax

    # ---------------------------
    # Register blueprints
    # ---------------------------
    from .auth.routes import bp as auth_bp
    from .main.routes import bp as main_bp
    from .customers.routes import bp as customer_bp
    from .suppliers.routes import bp as supplier_bp
    from .purchases.routes import bp as purchase_bp
    from .medicines.routes import bp as medicine_bp
    from .sales.routes import bp as sale_bp

    app.register_blueprint(main_bp, url_prefix="/")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(customer_bp, url_prefix="/customers")
    app.register_blueprint(supplier_bp, url_prefix="/suppliers")
    app.register_blueprint(purchase_bp, url_prefix="/purchases")
    app.register_blueprint(medicine_bp, url_prefix="/medicines")
    app.register_blueprint(sale_bp, url_prefix="/sales")

    # Make instance folder
    os.makedirs(app.instance_path, exist_ok=True)

    return app
