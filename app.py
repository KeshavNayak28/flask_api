from flask import Flask, request, Response, jsonify
from Database.post import Book
import json
from Database.database import Database


app = Flask(__name__)

'''initializes Database connection to deault port 27017'''
Database.intialize()

mongo_book = Book()



''' checks if the book to be added has specified fields'''
def validbook(bookObject):
    if ('name' in bookObject and 'price' in bookObject or '_id' in bookObject):
        return True
    else:
        return False



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
        return 'book with isbn {} not availaible'.format(isbn)
    else:
        books['_id'] = str(books['_id'])
        return jsonify(books)




'''Updates mongo book collection with specified isbn'''
@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_books(isbn):
    books = mongo_book.from_mongo(isbn)
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
        return jsonify(new_book)




'''Deletes a book from mongo collection with specified isbn'''
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    books = mongo_book.from_mongo(isbn)
    if books == None:
        return 'book with isbn {} not availaible '.format(isbn)
    else:
        mongo_book.delete_from_mongo(isbn)
        return 'deleted book with isbn {}'.format(isbn)





if __name__ == '__main__':
    app.run(debug=True)
