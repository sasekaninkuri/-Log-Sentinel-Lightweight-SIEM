# app/routes.py
from flask import Blueprint, render_template, send_file, make_response
import os, csv, io, json

main_bp = Blueprint('main', __name__)

def load_logs():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
    log_file = os.path.join(base_dir, 'logs', 'sample.log')  # adjust filename if needed
    events = []
    if not os.path.exists(log_file):
        return events
    with open(log_file, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) != 3:
                continue
            timestamp, level, message = parts
            is_suspicious = "failed" in message.lower() or "unauthorized" in message.lower() or "error" in level.lower()
            events.append({
                "timestamp": timestamp.strip(),
                "level": level.strip(),
                "message": message.strip(),
                "is_suspicious": is_suspicious
            })
    return events

@main_bp.route('/')
def dashboard():
    events = load_logs()
    suspicious_count = sum(e['is_suspicious'] for e in events)
    alert = suspicious_count > 0
    return render_template('dashboard.html', events=events, alert=alert, suspicious_count=suspicious_count)

@main_bp.route('/export/csv')
def export_csv():
    events = load_logs()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Timestamp', 'Level', 'Message', 'Suspicious'])
    for e in events:
        writer.writerow([e['timestamp'], e['level'], e['message'], 'Yes' if e['is_suspicious'] else 'No'])
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        as_attachment=True,
        attachment_filename='logs_export.csv',
        mimetype='text/csv'
    )

@main_bp.route('/export/json')
def export_json():
    events = load_logs()
    response = make_response(json.dumps(events, indent=4))
    response.headers['Content-Disposition'] = 'attachment; filename=logs_export.json'
    response.mimetype = 'application/json'
    return response


