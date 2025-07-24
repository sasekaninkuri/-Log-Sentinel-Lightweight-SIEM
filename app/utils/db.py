from app import mongo

def insert_log(log_data):
    """
    Insert a single log into the MongoDB 'logs' collection.
    """
    mongo.db.logs.insert_one(log_data)

def insert_bulk_logs(logs):
    """
    Insert multiple logs at once.
    """
    if logs:
        mongo.db.logs.insert_many(logs)

def get_all_logs():
    """
    Retrieve all logs from MongoDB.
    """
    return list(mongo.db.logs.find({}, {'_id': 0}))
