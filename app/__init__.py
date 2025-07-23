# app/__init__.py

from flask import Flask
from flask_pymongo import PyMongo
import os # Keep this import here for the debug print statement

# Initialize PyMongo globally
mongo = PyMongo()

def create_app():
    """
    Creates and configures the Flask application.
    """
    app = Flask(__name__)

    # --- DEBUG PRINT STATEMENT (Keep for now to confirm config loads) ---
    config_path = os.path.join(app.instance_path, 'config.py')
    print(f"DEBUG: Attempting to load config from: {config_path}")
    # --- END DEBUG PRINT STATEMENT ---

    # Load configuration from instance/config.py
    app.config.from_pyfile('config.py', silent=True)
    # It's good practice to set a SECRET_KEY, especially with Flash messages
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'your-very-secret-key-replace-me'

    # Initialize PyMongo with the app
    mongo.init_app(app)

    # Register Blueprints
    from app.routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    # This line is CRITICAL for Flask to find your app factory
    return app