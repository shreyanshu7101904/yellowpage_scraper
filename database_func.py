from pymongo import MongoClient
from datetime import date 
import json


def cursorObject():
    client = MongoClient()
    ref_coll = client.yellowpages_info
    return ref_coll

def documentObject(name, ref):
    ob = ref["yellowpages_data"]
    result = ob.find(name, {"Url":1, "Name":1,"_id":1})
    for i in result:
        print(i["_id"])


if __name__ == '__main__':
    db = cursorObject()
    
    print(str(date.today()))
    query = {
        "Date" : "2019-07-02"
    }
    documentObject(query, db)