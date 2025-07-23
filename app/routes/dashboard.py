# app/routes/dashboard.py

from flask import Blueprint, render_template, send_file, make_response, current_app
import os
import csv
import io
import json
import logging # Import logging for better error handling

# Set up basic logging (you might configure this more extensively in a real app)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

dashboard_bp = Blueprint('dashboard', __name__)

def load_logs():
    """
    Loads log events from the sample_syslog.log file,
    parses them, and identifies suspicious entries.
    """
    # Construct the path to the log file relative to the application root
    # This assumes 'logs' folder is one level up from 'app',
    # e.g., my_app/logs/sample_syslog.log
    # and this file is app/routes/dashboard.py
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    log_file_path = os.path.join(base_dir, 'logs', 'sample_syslog.log')

    events = []
    if not os.path.exists(log_file_path):
        logging.error(f"Log file not found at: {log_file_path}")
        # Optionally, you could flash a message to the user here
        return events

    try:
        with open(log_file_path, 'r', encoding='utf-8') as f: # Specify encoding
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line: # Skip empty lines
                    continue

                parts = line.split(',', 2) # Split only on the first two commas

                if len(parts) != 3:
                    logging.warning(f"Skipping malformed log line (line {line_num}): '{line}' - Expected 3 parts, got {len(parts)}")
                    continue

                timestamp = parts[0].strip()
                level = parts[1].strip()
                message = parts[2].strip() # The rest is the message

                is_suspicious = (
                    "failed" in message.lower()
                    or "unauthorized" in message.lower()
                    or "error" in level.lower()
                    or "denied" in message.lower() # Add more keywords as needed
                    or "access" in message.lower() and "fail" in message.lower()
                )
                events.append({
                    "timestamp": timestamp,
                    "level": level,
                    "message": message,
                    "is_suspicious": is_suspicious
                })
    except Exception as e:
        logging.error(f"Error reading or parsing log file {log_file_path}: {e}")
    return events

@dashboard_bp.route('/')
def dashboard():
    """
    Renders the main dashboard page, displaying log events and suspicious counts.
    """
    events = load_logs()
    suspicious_count = sum(1 for e in events if e['is_suspicious'])
    alert = suspicious_count > 0 # Simple alert flag if any suspicious events exist

    return render_template(
        'dashboard.html',
        events=events,
        alert=alert,
        suspicious_count=suspicious_count
    )

@dashboard_bp.route('/export/csv')
def export_csv():
    """
    Exports all log events as a CSV file.
    """
    events = load_logs()

    # Create an in-memory text buffer for the CSV data
    proxy = io.StringIO()
    writer = csv.writer(proxy)

    # Write the CSV header row
    writer.writerow(['Timestamp', 'Level', 'Message', 'Suspicious'])

    # Write each event as a row
    for event in events:
        writer.writerow([
            event['timestamp'],
            event['level'],
            event['message'],
            'Yes' if event['is_suspicious'] else 'No' # Convert boolean to 'Yes'/'No'
        ])

    # Create an in-memory binary buffer for the file content
    # This is required by send_file when passing a file-like object
    mem = io.BytesIO()
    # Write the UTF-8 encoded string content from StringIO to BytesIO
    mem.write(proxy.getvalue().encode('utf-8'))
    mem.seek(0) # Rewind the buffer to the beginning

    proxy.close() # Close the StringIO object

    return send_file(
        mem,
        as_attachment=True,
        download_name='logs_export.csv', # Filename for the download
        mimetype='text/csv' # MIME type for CSV files
    )

@dashboard_bp.route('/export/json')
def export_json():
    """
    Exports all log events as a JSON file.
    """
    events = load_logs()

    # Convert the list of event dictionaries to a JSON string
    json_output = json.dumps(events, indent=4) # indent for pretty-printing

    # Create a Flask response object
    response = make_response(json_output)

    # Set headers for file download
    response.headers['Content-Disposition'] = 'attachment; filename=logs_export.json'
    response.mimetype = 'application/json' # MIME type for JSON files

    return response