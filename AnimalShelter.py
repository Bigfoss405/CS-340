import os
from pymongo import MongoClient

class AnimalShelter(object):
    def __init__(self, username, password):
        # Retrieve MongoDB connection details
        HOST = os.getenv('MONGO_HOST', 'nv-desktop-services.apporto.com')
        PORT = int(os.getenv('MONGO_PORT', 30768))
        db = 'AAC' # Database name

        uri = f"mongodb://{username}:{password}@{HOST}:{PORT}/{db}?authSource=admin"
        self.client = MongoClient(uri)
        self.database = self.client[db]
        self.collection = self.database['animals']
        
    def read(self, query):
        return list(self.collection.find(query))

    # Create Method that inserts one document into the collection
    def create(self, data):
        if data:
            try:
                self.collection.insert_one(data)
                return True
            except Exception as e:
                print(f"Insert error: {e}") # Error check incase of failure
                return False
        else:
            raise Exception("No data to insert")

    # Read method that retrieves document based on query
    def read(self, query):
        try:
            cursor = self.collection.find(query if query else {})
            return list(cursor)
        except Exception as e:
            print(f"Read error: {e}") # Error check incase of failure
            return []

    # Update method that updates documents that matched query
    def update(self, query, update_data):
        if query and update_data:
            try:
                result = self.collection.update_many(query, {'$set': update_data})
                return result.modified_count
            except Exception as e:
                print(f"Update error: {e}") # Error check incase of failure
                return 0
        else:
            raise Exception("Query and update data must be provided")

    # Delete Method that deletes documents matching query
    def delete(self, query):
        if query:
            try:
                result = self.collection.delete_many(query)
                return result.deleted_count
            except Exception as e:
                print(f"Delete error: {e}") # Error check in case of failure
                return 0
        else:
            raise Exception("Query must be provided for delete")
