"""
App factory for the Flask application.
"""
from flask import Flask
from flask_cors import CORS
from .routes import routes

def create_app():
    """
    Creates and configures the Flask app.

    Returns:
        Flask: Configured Flask application.
    """
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(routes)
    return app
