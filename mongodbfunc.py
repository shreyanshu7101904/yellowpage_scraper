from pymongo import MongoClient
import datetime


def putDataInDb(doc, value):
    ob = MongoClient()
    value["Date"] = str(datetime.date.today())
    db = ob.yellowpages_info[doc]
    ids = db.insert_one(value).inserted_id

    print(ids)
def getUrlDataFromDb():

    query = {
        "Date": str(datetime.date.today())
    }

    client = MongoClient()
    ref_coll = client.yellowpages_info
    ob = ref_coll["yellowpages_data"]
    result = ob.find(query, {"Url":1})
    return result
        


if __name__ == '__main__':
    value = {
    "name": "abc",
    "link": "def"   
    }
    putDataInDb(value)