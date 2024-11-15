from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()


def create_app():
    """
    Creates and configures the Flask application.

    This function initializes a new Flask application, configures it with the settings from the Config object,
    initializes the database with the app, and registers the v1 blueprint.

    Returns:
        app: The initialized Flask application.
    """

    app = Flask(__name__)
    app.config.from_object('config.Config')

    from app.v1 import v1 as v1_blueprint
    app.register_blueprint(v1_blueprint, url_prefix='/api/v1')

    return app
