import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


def build_mysql_uri():
    """
    Build SQLAlchemy MySQL URI from env variables
    """
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "3307")
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    name = os.getenv("DB_NAME", "pharmacy_db")

    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}"


class BaseConfig:
    """Base configuration"""
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Internationalization
    BABEL_DEFAULT_LOCALE = os.getenv("BABEL_DEFAULT_LOCALE", "en")
    BABEL_DEFAULT_TIMEZONE = os.getenv("BABEL_DEFAULT_TIMEZONE", "Africa/Mogadishu")

    # Rate limiting
    RATELIMIT_DEFAULT = os.getenv("RATELIMIT_DEFAULT", "200/day;50/hour")

    # Mail configuration
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT") or 25)
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "False").lower() in ("1", "true", "yes")
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False").lower() in ("1", "true", "yes")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    try:
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or build_mysql_uri()
    except Exception:
        SQLALCHEMY_DATABASE_URI = "sqlite:///instance/app.db"


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    try:
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or build_mysql_uri()
    except Exception:
        SQLALCHEMY_DATABASE_URI = "sqlite:///instance/test.db"


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or build_mysql_uri()


def get_config(name: str = None):
    """
    Return the config class based on environment name
    """
    name = (name or "development").lower()
    if name in ("production", "prod"):
        return ProductionConfig
    if name in ("testing", "test"):
        return TestingConfig
    return DevelopmentConfig
