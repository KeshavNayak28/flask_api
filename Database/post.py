from Database.database import Database

class Book:
    def __init__(self, name:str=None , price:int=None , isbn=None , _id=None):
        self.name = name
        self.price = price
        self.isbn = isbn
        self._id = _id


    @staticmethod
    def add_to_mongo_directly(data):
        mongo_data=Database.insert(collection='posts', data=data)
        return mongo_data

    @staticmethod
    def from_mongo(query):
        mongo_data = Database.find_one(collection='posts', query={'isbn':int(query)})
        print(mongo_data)
        return dict(mongo_data)

    @staticmethod
    def update_mongo_book(query, updates):
        Database.update(collection='posts', myquery={'isbn':int(query)}, updates={'$set':updates})

    @staticmethod
    def delete_from_mongo(query):
        Database.delete_one(collection='posts', query={'isbn':int(query)})