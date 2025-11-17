import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

from .extensions import db, migrate, login_manager, mail, babel, limiter
from .config import get_config
from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"

def create_app(config_name=None):
    app = Flask(__name__, instance_relative_config=False)
    cfg = get_config(os.getenv("FLASK_ENV", "development"))
    app.config.from_object(cfg)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    babel.init_app(app)
    limiter.init_app(app)

    from .auth import bp as auth_bp
    from .main import bp as main_bp
    
    app.register_blueprint(main_bp)
    
    app.register_blueprint(auth_bp, url_prefix="/auth")
    os.makedirs(app.instance_path, exist_ok=True)
    return app
