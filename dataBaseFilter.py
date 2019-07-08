from pymongo import MongoClient


def insertDataToDb(data):
    insert_ob = MongoClient()
    db = insert_ob["final"]["Final"]
    print(db.insert_one(data).inserted_id, "id")


def createSetCollection(data):
    unq = set()
    for i in data:
        unq.add(i["population"])
        print(i["population"])
        if len(unq) > 1:
            insertDataToDb(data[0])
    insertDataToDb(data[0])


def convertData(cat, loc):
    data = {}
    # loca = city_state, population
    # cat = search_category, Search Volum
    data["location"] = loc["city_state"]
    data['population'] = loc["population"]
    data['category'] = cat["search_category"]
    data["combination"] = loc["city_state"] + '/' + cat["search_category"]
    data["weight"] = cat["Search Volume"]
    data["multiply"] = int(loc['population']) * int(cat['Search Volume'])
    insertDataToDb(data)
    # print(data)


def filterdatabase():
    obl = MongoClient()
    dbl = obl["final"]["location"]
    obc = MongoClient()
    dbc = obc["final"]["categories"]
    # print(db.aggregate(distinct_pipeline, allowDiskUse=True))
    # for i in db.aggregate(distinct_pipeline, allowDiskUse=True):
    for loc in dbl.find():
        for cat in dbc.find():
            convertData(cat, loc)
            # print(j["Search Volume"], i) 
            # loca = city_state, population
            # cat = search_category, Search Volume


if __name__ == '__main__':
    filterdatabase()