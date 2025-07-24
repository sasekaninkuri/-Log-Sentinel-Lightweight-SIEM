import os
import logging

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_logs():
    """
    Loads and parses log entries from a log file, detecting suspicious events.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    log_file_path = os.path.join(base_dir, 'logs', 'sample_syslog.log')

    events = []
    if not os.path.exists(log_file_path):
        logging.error(f"Log file not found at: {log_file_path}")
        return events

    try:
        with open(log_file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue

                parts = line.split(',', 2)
                if len(parts) != 3:
                    logging.warning(f"Malformed line {line_num}: '{line}'")
                    continue

                timestamp = parts[0].strip()
                level = parts[1].strip()
                message = parts[2].strip()

                is_suspicious = (
                    "failed" in message.lower()
                    or "unauthorized" in message.lower()
                    or "error" in level.lower()
                    or "denied" in message.lower()
                    or ("access" in message.lower() and "fail" in message.lower())
                )

                events.append({
                    "timestamp": timestamp,
                    "level": level,
                    "message": message,
                    "is_suspicious": is_suspicious
                })
    except Exception as e:
        logging.error(f"Error reading/parsing log file {log_file_path}: {e}")
    return events
