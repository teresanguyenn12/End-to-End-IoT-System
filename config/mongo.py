from pymongo import MongoClient
import certifi

def get_db():
    # MongoDB connection URI
    try: 
        uri = "mongodb+srv://dylanswanson01:Password123@cluster0.wnjbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
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