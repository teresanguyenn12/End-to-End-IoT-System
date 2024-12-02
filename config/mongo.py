from pymongo import MongoClient
import certifi
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MONGO_CONNECTION_URI = os.getenv("MONGO_CONNECTION_URI")

def get_db():
    # MongoDB connection URI
    try: 
        uri = str(MONGO_CONNECTION_URI)
        client = MongoClient(uri, tlsCAFile=certifi.where())
        db = client['test']
        print("Connected to MongoDB")
    except Exception as e:
        print(f"An error occurred in get_db: {e}")
    return db

# Example function to get a collection from the DB
def get_collection(collection_name):
    db = get_db()
    return db[collection_name]

def get_refrigerator_data() -> list:
    print("Getting refrigerator data...")
    collection = get_collection("devices_virtual")
    data = collection.find() 
    return list(data)

def get_avg_refrigerator_moisture():
    print("Getting average refrigerator moisture...")
    collection = get_collection("devices_virtual")
    data = collection.aggregate([{"$group": {"_id": None, "avgMoisture": {"$avg": "$moisture"}}}])
    return list(data)