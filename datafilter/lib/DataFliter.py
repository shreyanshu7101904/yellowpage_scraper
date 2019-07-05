from pymongo import MongoClient


class DataFilter:

    def __init__(self, db, collection):
        self.db = db
        self.collection = collection

    def getData(self):
        ob = MongoClient()
        data_base = ob.yellowpages_info["yellowpages_data"]
        print(data_base.find_one())

    def createCursorObject(self):
        ob = MongoClient()
        data_base = ob[self.db][self.collection]
        print(len([i for i in data_base.distinct("id")]))
        for i in data_base.distinct("id"):
            print(i, "\n\n")
        # for i in data_base.find():
        #     print(i)


if __name__ == '__main__':
    obj = DataFilter("yellowpages_info", "yellowpages_data")
    obj.createCursorObject()
    obj.getData()

    