from flask import Flask
from flask_pymongo import PyMongo
import os

# Initialize PyMongo globally
mongo = PyMongo()

def create_app():
    """
    Creates and configures the Flask application.
    """
    app = Flask(__name__, instance_relative_config=True)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError as e:
        print(f"DEBUG: Could not create instance folder: {e}")

    # Debug statement to confirm config path
    config_path = os.path.join(app.instance_path, 'config.py')
    print(f"DEBUG: Attempting to load config from: {config_path}")

    # Load configuration from instance/config.py (optional)
    app.config.from_pyfile('config.py', silent=True)

    # Set default SECRET_KEY and MONGO_URI if not already set
    app.config.setdefault('SECRET_KEY', 'super-secure-secret-key')
    app.config.setdefault('MONGO_URI', 'mongodb://localhost:27017/log_sentinel')

    # Initialize PyMongo with the app
    mongo.init_app(app)

    # Register Blueprints
    from app.routes.dashboard import dashboard_bp
    from app.routes.dashboard_file import dashboard_file_bp

    app.register_blueprint(dashboard_bp)          # MongoDB routes (e.g., /, /export/csv)
    app.register_blueprint(dashboard_file_bp)     # File-based routes (e.g., /file-dashboard)

    return app

