from Database.database import Database


class User:


    @staticmethod
    def add_user(data):
        user_mongo_data=Database.insert_mongo(collection='users', data=data)
        return user_mongo_data


    @staticmethod
    def get_user(query):
        user_mongo_data = Database.find_one(collection='users', query = {'user_id': query})
        return user_mongo_data


    @staticmethod
    def find_all_mongo(query):
        mongo_user = Database.find(collection='users', query = {'email':str(query)})
        print(mongo_user)
        return mongo_user