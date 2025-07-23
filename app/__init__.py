# Open app/__init__.py for editing
# nano app/__init__.py

# Change its content to:
# app/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import and register the dashboard blueprint
    # Note the change from 'app.routes' to 'app.routes.dashboard'
    from app.routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    return app




