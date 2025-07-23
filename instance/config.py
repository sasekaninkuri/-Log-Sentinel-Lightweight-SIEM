# instance/config.py

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

LOG_FILE_PATH = os.path.join(BASE_DIR, 'logs', 'sample.log')
EXPORT_PATH = os.path.join(BASE_DIR, 'exports')
ALERT_THRESHOLD = 1
MONGO_URI="mongodb+srv://sasekaninkuri560:6y7b6a8jpzSU2JDe@cluster0.kdaauok.mongodb.net/Sasekanidb"