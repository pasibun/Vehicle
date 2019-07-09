import pymongo


class DatabaseHelper:
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    dbName = "Hexapod"
    mydb = myclient[dbName]

    def dbCheck(self):

        dblist = self.myclient.list_database_names()

        if self.dbName in dblist:
            return True
        else:
            print("Database bestaat niet")
            return False

    def insertDate(self, collection, data):
        if self.dbCheck():
            col = self.mydb[collection]
            insertData = col.insert_many(data)
            return insertData.inserted_ids
        else:
            return None
