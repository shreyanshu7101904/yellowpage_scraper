from pymongo import MongoClient
from datetime import date



def putDataInDb(doc, value):
    ob = MongoClient('mongodb://admin:new_password_here@localhost:27017/')
    value["Date"] = str(date.today())
    db = ob.yellowpages_info[doc]
    ids = db.insert_one(value).inserted_id
    # 
    # print(ids)

value = {
    "name": "abc",
    "link": "def"
}
if __name__ == '__main__':
    putDataInDb(value)