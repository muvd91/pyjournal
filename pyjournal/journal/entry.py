import time
import datetime


class Entry:
    def __init__(self, log=None):
        if log is None:
            self.content = ""
            self.timestamp = 0
            self.tags = list()
            self.category = ""
            self.file_id = None
            return
        self.content = log['content']
        self.timestamp = log['timestamp']
        self.tags = log['tags']
        self.category = log['category']
        self.file_id = log['file_id']
        self._id = str(log['_id'])

    def set_content(self, content):
        self.content = content

    def set_category(self, entry_category):
        self.category = entry_category

    def set_tag(self, tags):
        self.tags = tags

    def set_timestamp(self, ts=time.time()):
        self.timestamp = ts

    def set_file_id(self, file_id):
        self.file_id = str(file_id) if file_id is not None else None

    def get_date_from_ts(self):
        date = datetime.datetime.fromtimestamp(self.timestamp)
        return date.day, date.month, date.year
