from pymongo import MongoClient
from datetime import date 
import json


def cursorObject():
    client = MongoClient()
    ref_coll = client.yellowpages_info
    return ref_coll

def documentObject(name):
    client = MongoClient()
    ref_coll = client.yellowpages_info
    ob = ref_coll["yellowpages_data"]
    result = ob.find(name, {"Url":1, "Name":1,"_id":1})
    for i in result:
        print(i["_id"])

def findById(ids):
    client = MongoClient()
    ref_coll = client.yellowpages_info
    ob = ref_coll["yellowpages_data"]
    result = ob.findOne({}, {"Url":1, "Name":1,"_id":1})
    for i in result:
        print(i["_id"])


if __name__ == '__main__':

    query = {
        "_id" : "5d1dd74a1ca65d9980a50389"
    }
    findById(query)