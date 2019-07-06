from pymongo import MongoClient

client = MongoClient("mongodb://admin:new_password_here@localhost:27017/")
db = client.yellowpages_info
yellowpages_data = db.yellowpages_data


def CheckData(id):
    data = yellowpages_data.find()
    ids = []
    for d in data :
        ids.append(d["id"])
    print(len(ids))
