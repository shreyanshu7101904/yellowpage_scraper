from pymongo import MongoClient



def putDataInDb(doc, value):
    ob = MongoClient()
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