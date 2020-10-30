"""App configuration."""
VERSION = "0.8.1"


from os import environ, path

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5000


basedir = path.abspath(path.dirname(__file__))


class Config:
    """Set Flask configuration vars from .env file."""

    # General Config
    SECRET_KEY = environ.get("SECRET_KEY", "asdasda")
    FLASK_APP = environ.get("FLASK_APP", "VUPEC")
    FLASK_ENV = environ.get("FLASK_ENV", "DEV")

    # Static Assets
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
