from flask import Blueprint, render_template, send_file, make_response
import os
import csv
import io
import json

dashboard_bp = Blueprint('dashboard', __name__)

def load_logs():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    log_file = os.path.join(base_dir, 'logs', 'sample_syslog.log')
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
                "failed" in message.lower()
                or "unauthorized" in message.lower()
                or "error" in level.lower()
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

@dashboard_bp.route('/export/csv')
def export_csv():
    events = load_logs()

    # Create in-memory CSV file
    proxy = io.StringIO()
    writer = csv.writer(proxy)
    writer.writerow(['Timestamp', 'Level', 'Message', 'Suspicious'])
    for event in events:
        writer.writerow([
            event['timestamp'],
            event['level'],
            event['message'],
            'Yes' if event['is_suspicious'] else 'No'
        ])

    mem = io.BytesIO()
    mem.write(proxy.getvalue().encode('utf-8'))
    mem.seek(0)
    proxy.close()

    return send_file(
        mem,
        as_attachment=True,
        download_name='logs_export.csv',
        mimetype='text/csv'
    )


@dashboard_bp.route('/export/json')
def export_json():
    events = load_logs()

    response = make_response(json.dumps(events, indent=4))
    response.headers['Content-Disposition'] = 'attachment; filename=logs_export.json'
    response.mimetype = 'application/json'

    return response

