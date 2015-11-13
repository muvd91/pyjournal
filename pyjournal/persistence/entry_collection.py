from datetime import datetime
from time import time
from bson import ObjectId
from bson.errors import InvalidId
import persistence.db
import pymongo

from journal.entry import Entry


class EntryCollection:
    def __init__(self):
        self.collection = persistence.db.get_collection('entries')

    def count(self):
        return self.collection.count()

    def get_single_date_logs(self, day=-1, month=-1, year=-1):
        if year == -1:
            year = datetime.fromtimestamp(time()).year
        if month == -1:
            month = datetime.fromtimestamp(time()).month
        if day == -1:
            day = datetime.fromtimestamp(time()).day
        t1 = datetime(year, month, day).timestamp()
        t2 = datetime(year, month, day, 23, 59).timestamp()
        query = {"timestamp": {"$gt": t1}, "timestamp": {"$lt": t2}}
        return self.collection.find(query)

    def get_all_logs(self):
        logs = self.collection.find().sort([("timestamp", pymongo.ASCENDING)])
        response = []
        for l in logs:
            response.append(Entry(l))
        return response

    def insert(self, entry):
        entry_dict = entry.__dict__
        if entry_dict['file_id'] is not None:
            entry_dict['file_id'] = ObjectId(entry_dict['file_id'])
        self.collection.insert_one(entry_dict)
        entry_dict['_id'] = str(entry_dict['_id'])
        return entry

    def find(self, dict_query):
        logs = self.collection.find(dict_query).sort([("timestamp", pymongo.ASCENDING)])
        response = list()
        for l in logs:
            response.append(Entry(l))
        return response

    def delete_one(self, dict_query):
        return self.collection.delete_one(dict_query).deleted_count

    def find_one(self, dict_query):
        try:
            dict_query['_id'] = ObjectId(dict_query['_id'])
        except InvalidId:
            return None
        document = self.collection.find_one(dict_query)
        if document is None:
            return None
        return Entry(document)

    def update_one(self, dict_query, updated_entry):
        del updated_entry._id
        updated_entry = updated_entry.__dict__
        return self.collection.replace_one(dict_query, updated_entry).modified_count

    def find_with_projection(self, query, projection):
        return self.collection.find(query, projection)
