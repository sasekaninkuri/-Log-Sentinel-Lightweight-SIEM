
from flask import Blueprint, render_template, send_file, make_response, jsonify
from app.utils.db import get_all_logs
import csv, io, json

dashboard_bp = Blueprint('dashboard', __name__)

# ─────────────────────────────────────────────
# 🧠 ROUTES
# ─────────────────────────────────────────────

@dashboard_bp.route('/')
def dashboard():
    events = get_all_logs()
    suspicious_count = sum(1 for e in events if e.get('is_suspicious'))
    alert = suspicious_count > 0

    return render_template(
        'dashboard.html',
        events=events,
        alert=alert,
        suspicious_count=suspicious_count
    )

@dashboard_bp.route('/export/csv')
def export_csv():
    events = get_all_logs()

    proxy = io.StringIO()
    writer = csv.writer(proxy)
    writer.writerow(['Timestamp', 'Level', 'Message', 'Suspicious'])

    for event in events:
        writer.writerow([
            event.get('timestamp'),
            event.get('level'),
            event.get('message'),
            'Yes' if event.get('is_suspicious') else 'No'
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
    events = get_all_logs()
    response = make_response(json.dumps(events, indent=4))
    response.headers['Content-Disposition'] = 'attachment; filename=logs_export.json'
    response.mimetype = 'application/json'
    return response

@dashboard_bp.route('/compliance')
def compliance():
    return jsonify({
        "NIST_CSF": {
            "Identify": "ID.AM-1: Asset management for logs and hosts",
            "Detect": "DE.CM-1: Real-time monitoring of logs",
            "Respond": "RS.AN-1: Alerts generated on suspicious activity",
            "Recover": "RC.CO-1: Exporting logs to assist recovery"
        },
        "ISO_27001": {
            "A.12.4.1": "Event logging enabled",
            "A.16.1.2": "Incident detection and alerting"
        }
    })
