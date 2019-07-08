from pymongo import MongoClient


class DataFilter:

    def __init__(self, db, base_collection, intermediate_collection):
        self.db = db
        self.base_collection = base_collection
        self.intermediate_collection = intermediate_collection


    def insertDataToDb(self, data):
        insert_ob = MongoClient()
        db = insert_ob[self.db][self.intermediate_collection]
        print(db.insert_one(data).inserted_id, "id")


    def checkDataInIntermediateDB(self, value):
        mongo_ob = MongoClient()
        db = mongo_ob[self.db][self.intermediate_collection]
        if db.find({"business_id":value}).count() != 0:
            return True
        else:
            return False


    def createCursorObject(self):
        ob = MongoClient()
        data_base = ob[self.db][self.base_collection]
        distinct_pipeline = [
            {"$group": {"_id": "$business_id","data":{"$push":"$$ROOT"} }}
            ]
        
        for i in data_base.aggregate(distinct_pipeline, allowDiskUse=True):
            # print(i["data"][0])
            check_val = self.checkDataInIntermediateDB(i["data"][0]["business_id"])
            if check_val:
                print("value already exists")
            else:
                self.insertDataToDb(i["data"][0])



    def pullAndPushData(self):
        self.createCursorObject()


def generateLinks():
    links = []
    level_one = MongoClient()
    level_one = level_one.level_one_db.data 
    data = level_one.find()
    for i in data:
        links.append("https://www.yellowpages.com"+"/"+ i["city_state"] + "/" + i["category"])
    return links
                


if __name__ == '__main__':
    generateLinks()

    