from pymongo import MongoClient

def get_mongo_connection(uri):
    """Return a MongoDB client instance."""
    return MongoClient(uri)
