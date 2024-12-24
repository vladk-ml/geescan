import os

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

def create_app():
    """
    Creates and configures the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """

    app = Flask(__name__)

    # Enable Cross-Origin Resource Sharing (CORS)
    CORS(app)

    # Database configuration from environment variables
    app.config['DB_HOST'] = os.environ.get('DB_HOST')
    app.config['DB_PORT'] = os.environ.get('DB_PORT')
    app.config['DB_NAME'] = os.environ.get('DB_NAME')
    app.config['DB_USER'] = os.environ.get('DB_USER')
    app.config['DB_PASSWORD'] = os.environ.get('DB_PASSWORD')

    # Register the API Blueprint (routes defined in routes.py)
    from app.api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app