# app/routes/dashboard_file.py

from flask import Blueprint, render_template
from app.utils.file_logs import load_logs

dashboard_file_bp = Blueprint('dashboard_file', __name__)

@dashboard_file_bp.route('/dashboard_file')
def dashboard_file():
    logs = load_logs()
    return render_template('dashboard_file.html', logs=logs)

