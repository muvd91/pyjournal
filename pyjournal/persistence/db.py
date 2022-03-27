from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os

MONGO_DIR = os.path.expandvars('${HOME}/pyjournal/data/mongo_db.conf')
MONGO_HOST = 'localhost'
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
    client = MongoClient()
    try:
        # The ping command is cheap and does not require auth.
        client.admin.command('ping')
    except ConnectionFailure:
        print("Server not available")
        exit()


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
