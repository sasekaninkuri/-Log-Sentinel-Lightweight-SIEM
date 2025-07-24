from datetime import datetime
from collections import namedtuple

LogEvent = namedtuple('LogEvent', ['timestamp', 'level', 'message', 'is_suspicious'])

def parse_log_line(line):
    try:
        parts = line.strip().split('|')
        timestamp = datetime.strptime(parts[0], '%Y-%m-%d %H:%M:%S')
        level = parts[1].strip()
        message = parts[2].strip()
        is_suspicious = any(keyword in message.lower() for keyword in ['unauthorized', 'failed', 'error', 'malicious'])
        return LogEvent(timestamp, level, message, is_suspicious)
    except Exception:
        return None

def load_logs(log_file_path='logs/system.log'):
    events = []
    suspicious_count = 0
    try:
        with open(log_file_path, 'r') as f:
            for line in f:
                event = parse_log_line(line)
                if event:
                    events.append(event)
                    if event.is_suspicious:
                        suspicious_count += 1
    except FileNotFoundError:
        print(f"[!] Log file not found: {log_file_path}")
    return events, suspicious_count
