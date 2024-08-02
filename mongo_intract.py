from pymongo import MongoClient
import certifi

MONGO_URI = 'mongodb+srv://piroop:piroop@piro.hexrg9w.mongodb.net/?retryWrites=true&w=majority&appName=piro&tlsAllowInvalidCertificates=true'
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client['soul']
users_collection = db.users
keys_collection = db.keys
new_collection = db.users_new

def listCollection():
    collection_names = db.list_collection_names()

    print("Collections in the database:")
    for name in collection_names:
        print(name)

def printCollection(col):
    result = list(col.find())
    print(result)
    print(len(result))

def deleteAll(col):
    col.delete_many({})




printCollection(users_collection)