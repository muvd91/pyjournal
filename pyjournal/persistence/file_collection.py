import persistence.db


class FileCollection:
    def __init__(self):
        self.collection = persistence.db.get_collection('files')

    def insert(self, file_document):
        self.collection.insert_one(file_document)
        file_document['_id'] = str(file_document['_id'])
        return file_document

    def count(self):
        return self.collection.count()

    def get_all_files(self):
        return self.collection.find()

    def find(self, file_id):
        return self.collection.find({'_id': file_id}).sort()

    def edit(self, file_id, new_file):
        del new_file._id
        return self.collection.replace_one({'_id': file_id}, new_file).modified_count

    def delete(self, file_id):
        return self.collection.delete_one({'_id': file_id}).deleted_count

