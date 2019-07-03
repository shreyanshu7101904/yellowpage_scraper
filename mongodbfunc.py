from pymongo import MongoClient



def putDataInDb(value):
    ob = MongoClient()
    db = ob.yellowpages_info.yellowpages_data
    ids = db.insert_one(value).inserted_id
    # 
    # print(ids)


value = {
    "name": "abc",
    "link": "def"
}
if __name__ == '__main__':
    putDataInDb(value)