from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os

MONGO_DIR = os.path.expandvars('${HOME}/pyjournal/data/mongo_db.conf')
MONGO_HOST = 'db'
MONGO_DB = 'journal'

database_name = None
client = None
db_conn = None


def connect_to_db(db_host=MONGO_HOST, db_name=MONGO_DB):
    print("Connecting to MongoClient")
    global database_name
    database_name = db_name
    global client
    client = MongoClient(host=db_host)
    global db_conn
    db_conn = client[database_name]

    attempts = 0
    while attempts < 3:
        try:
            client.admin.command('ping')
            break
        except ConnectionFailure:
            attempts += 1
            if attempts == 3:
                exit("Couldn't connect to a mongo instance")
            print("Server not available. Attempting connection again...")

def get_collection(coll):
    global client
    global db_conn
    if client is None:
        raise ConnectionFailure('No connection established')
    return db_conn[coll]


def ping_db():
    global client
    try:
        client[database_name].command('ping')
    except ConnectionFailure:
        return False
    return True


def close_connection():
    global client
    print("Closing MongoClient")
    client.close()


connect_to_db()
