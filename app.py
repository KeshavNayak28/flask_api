from flask import Flask, request, Response, jsonify
from Database.post import Book
from Database.database import Database
from Database.login import User
from Database.purchase import Purchase
import datetime
import json


app = Flask(__name__)


'''initializes Database connection to deault port 27017'''
Database.intialize()



'''calls the Book class and User class in databse.py'''
mongo_book = Book()
mongo_user = User()
mongo_purchase = Purchase()



''' checks if the book to be added has specified fields'''
def validbook(bookObject):
    if ('name' in bookObject and 'price' in bookObject or '_id' in bookObject):
        return True
    else:
        return False


'''-----------------------------------------Users collection---------------------------------------------------------'''

def validate_user(userObject):
    if 'user_name' in userObject and 'email' in userObject and 'user_id' in userObject:
        return True
    else:
        return False

'''creates a user and checks if he already exists'''
@app.route('/users', methods=['POST'])
def create_user():
    user = request.get_json()
    if validate_user(user):
        user_check = get_user_by_user_id(user['user_id'])
        email_check = mongo_user.find_all_mongo(user['email'])
        if len(email_check)>0:
            return 'email {} already exists'.format(user['email'])
        if user_check == 'user doesnt exist':
            User.add_user(user)
            return get_user_by_user_id(user['user_id'])
        else:
            return 'user exists'
    else:
        error_message ={
            'error message':'invalid user passed',
            "helpstring": "needs to be in form: {'user_name': string,    'email': str , 'user_id': unique_int}"
        }
        return error_message, 400


'''Gives user with specified id'''
@app.route('/users/<user_id>', methods=['GET'])
def get_user_by_user_id(user_id):
    mongo_collection = mongo_user.get_user(user_id)
    if mongo_collection == None:
        return 'user doesnt exist'
    else:
        mongo_collection['_id'] = str(mongo_collection['_id'])
        return mongo_collection


''''---------------------------------------Purchase collection-------------------------------------------------------'''


@app.route('/purchase/<user_id>/<isbn>', methods=['GET'])
def user_purchase_book(user_id, isbn):
    ls=[]
    user_detail = get_user_by_user_id(user_id)
    user = {
            'user_name':user_detail['user_name'],
            'user_id':user_detail['user_id'],
            'email': user_detail['email']
    }
    book_choice = get_book_by_isbn(isbn)
    book = {
            'name' : book_choice['name'],
            'price': book_choice['price'],
            'isbn' : book_choice['isbn'],
            'date_of_purchase': datetime.datetime.now()
    }
    user.update({'purchase_detail':book})
    ls.append(user)
    mongo_purchase.add_mongo_purchase(ls)
    user['_id'] = str(user['_id'])
    return user


@app.route('/purchase/details/<user_id>', methods=['GET'])
def user_purchase_detail(user_id):
    all_purchases = mongo_purchase.from_mongo_purchase(user_id)
    if len(all_purchases)>0:
        return jsonify(all_purchases)
    else:
        return 'No Purchases'




'''------------------------------------Books Collection--------------------------------------------------------------'''


'''Adds single book or list of books with specified field to mongo'''
@app.route('/books', methods=['POST'])
def add_books():
    new_collection = []
    ls=[]
    books =  request.get_json()
    for book in books:
        if validbook(book):
            new_books = {
                'name': book['name'],
                'price': book['price'],
                'isbn': book['isbn']
            }
            new_books.update({'date_of_creation':datetime.datetime.now()})
            isbn=new_books['isbn']
            collection = mongo_book.from_mongo(isbn)
            if collection == None:
                mongo_book.add_to_mongo_directly(new_books)
                new_books['_id']= str(new_books['_id'])
                new_collection.append(new_books)
            else:
                ls.append(new_books)
        else:
            invalidBookErrorMsg  = {
                "error" : "invalid book passed",
                "helpstring" : "needs to be in form: {name:'bookname', 'price': int , 'isbn': UUID}"
            }
            response = Response(json.dumps(invalidBookErrorMsg), status=400, mimetype='application/json')
            return response
    if len(books) == len(new_collection):
        return jsonify(new_collection), 200
    else:
        return 'books below sent to mongo \n {0} \n books below already exist \n {1} '.format(new_collection, ls)



'''Gives the book with specified isbn from mongo'''
@app.route('/books/<int:isbn>', methods=['GET'])
def get_book_by_isbn(isbn):
    books=mongo_book.from_mongo(isbn)
    if books == None:
        return 'book with isbn {} not availaible'.format(isbn), 400
    else:
        books['_id'] = str(books['_id'])
        return books




'''Updates mongo book collection with specified isbn'''
@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_books(isbn):
    books = mongo_book.from_mongo(isbn)
    print(books)
    if books == None:
        return 'book with isbn {} not availaible '.format(isbn)
    else:
        update_book = request.get_json()
        new_book={}
        if 'name' in update_book:
            new_book['name'] = update_book['name']
        if 'price' in update_book:
            new_book['price'] = update_book['price']
        mongo_book.update_mongo_book(isbn, new_book)
        return get_book_by_isbn(isbn)




'''Deletes a book from mongo collection with specified isbn'''
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    books = mongo_book.from_mongo(isbn)
    if books == None:
        return 'book with isbn {} not availaible '.format(isbn), 400
    else:
        mongo_book.delete_from_mongo(isbn)
        return 'deleted book with isbn {}'.format(isbn), 200



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
