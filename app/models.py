# app/models.py

from dataclasses import dataclass
from datetime import datetime

@dataclass
class LogEvent:
    timestamp: datetime
    level: str
    message: str
    is_suspicious: bool

def parse_log_line(line: str):
    # Expected format: timestamp,level,message
    parts = line.split(',')
    if len(parts) != 3:
        return None
    timestamp_str, level, message = parts
    try:
        timestamp = datetime.strptime(timestamp_str.strip(), '%Y-%m-%d %H:%M:%S')
    except ValueError:
        # fallback if timestamp format differs or invalid
        timestamp = datetime.now()
    level = level.strip()
    message = message.strip()
    is_suspicious = (
        "failed" in message.lower() or
        "unauthorized" in message.lower() or
        "error" in level.lower()
    )
    return LogEvent(timestamp, level, message, is_suspicious)
