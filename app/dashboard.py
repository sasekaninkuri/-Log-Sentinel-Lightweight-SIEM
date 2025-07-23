from flask import Blueprint, render_template
import os

dashboard_bp = Blueprint('dashboard', __name__)

def load_logs():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    log_file = os.path.join(base_dir, 'logs', 'sample.log')  # your file is sample.log not sample_syslog.log

    events = []

    if not os.path.exists(log_file):
        return events

    with open(log_file, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) != 3:
                continue
            timestamp, level, message = parts
            is_suspicious = (
                "failed" in message.lower() or
                "unauthorized" in message.lower() or
                "error" in level.lower()
            )
            events.append({
                "timestamp": timestamp.strip(),
                "level": level.strip(),
                "message": message.strip(),
                "is_suspicious": is_suspicious
            })
    return events

@dashboard_bp.route('/')
def dashboard():
    events = load_logs()
    suspicious_count = sum(1 for e in events if e['is_suspicious'])
    alert = suspicious_count > 0
    return render_template('dashboard.html', events=events, alert=alert, suspicious_count=suspicious_count)
