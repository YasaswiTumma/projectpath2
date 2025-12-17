import os
import json
from dotenv import load_dotenv

load_dotenv()

# Simple JSON file-based storage for demo purposes
class JSONDatabase:
    def __init__(self, db_file='path2placement_db.json'):
        self.db_file = db_file
        self.data = self._load_data()

    def _load_data(self):
        try:
            with open(self.db_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'users': []}

    def _save_data(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def users(self):
        return JSONCollection(self, 'users')

class JSONCollection:
    def __init__(self, db, collection_name):
        self.db = db
        self.collection_name = collection_name

    def insert_one(self, document):
        if self.collection_name not in self.db.data:
            self.db.data[self.collection_name] = []
        document['_id'] = str(len(self.db.data[self.collection_name]) + 1)
        self.db.data[self.collection_name].append(document)
        self.db._save_data()
        return type('Result', (), {'inserted_id': document['_id']})()

    def find_one(self, query):
        if self.collection_name not in self.db.data:
            return None
        for item in self.db.data[self.collection_name]:
            if all(item.get(k) == v for k, v in query.items()):
                return item
        return None

    def find(self, query=None):
        if self.collection_name not in self.db.data:
            return []
        if query is None:
            return self.db.data[self.collection_name]
        return [item for item in self.db.data[self.collection_name]
                if all(item.get(k) == v for k, v in query.items())]

    def update_one(self, query, update):
        if self.collection_name not in self.db.data:
            return
        for i, item in enumerate(self.db.data[self.collection_name]):
            if all(item.get(k) == v for k, v in query.items()):
                self.db.data[self.collection_name][i].update(update['$set'])
                self.db._save_data()
                return

    def delete_one(self, query):
        if self.collection_name not in self.db.data:
            return
        for i, item in enumerate(self.db.data[self.collection_name]):
            if all(item.get(k) == v for k, v in query.items()):
                del self.db.data[self.collection_name][i]
                self.db._save_data()
                return

# Use JSON database instead of MongoDB
_db_instance = None

def get_db():
    global _db_instance
    if _db_instance is None:
        _db_instance = JSONDatabase()
    return _db_instance

# For compatibility with existing code that expects db.users to be a collection
class CompatibilityDB:
    def __init__(self, json_db):
        self._json_db = json_db

    @property
    def users(self):
        return self._json_db.users()

# Return compatibility wrapper
def get_db_compat():
    global _db_instance
    if _db_instance is None:
        _db_instance = JSONDatabase()
    return CompatibilityDB(_db_instance)
