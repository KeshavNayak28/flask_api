from Database.database import Database


class Purchase:

    @staticmethod
    def add_mongo_purchase(data):
        purchase_data = Database.insert_mongo(collection='purchase', data=data)
        return purchase_data

    @staticmethod
    def find_user_id(query):
        ls = []
        user_detail = [user_detail for user_detail in
                       Database.find(collection='purchase', query={'user_id': int(query)})]
        for i in user_detail:
            i['_id'] = str(i['_id'])
            ls.append(i)

    @staticmethod
    def from_mongo_purchase(user_id):
        ls = []
        pipeline = ([
            {"$match":{"user_id":int(user_id)}},
            {"$group":
                 {"_id": int(user_id),
                  "purchases": {"$addToSet": "$purchase_detail"}, "email": {"$first": "$email"}
                  }},
            {"$project": {"purchases": 1, "_id": 1, "email": 1}}
        ])
        user_purchases = Database.aggregate(collection='purchase', pipeline=pipeline)
        for i in user_purchases:
            ls.append(i)
        return ls
