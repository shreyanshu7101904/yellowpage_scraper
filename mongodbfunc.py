from pymongo import MongoClient
import datetime


def putDataInDb(doc, value):
    ob = MongoClient()
    value["Date"] = str(datetime.date.today())
    db = ob.yellowpages_info[doc]
    ids = db.insert_one(value).inserted_id
    # 
    # print(ids)


if __name__ == '__main__':
    value = {
    "name": "abc",
    "link": "def"   
    }
    putDataInDb(value)