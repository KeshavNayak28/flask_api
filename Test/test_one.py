from http.server import HTTPServer
import requests
import json


def test_passing():
    assert (1,2,3) == (1,2,3)

def test_mongo_add_book():
    print('hello')
    payload=[{'name': 'inviz_test',
         'price': 456,
          'isbn':419
          }]
    response = requests.request("POST", 'http://localhost:5000/books', data=json.dumps(payload) ,headers = {'Content-Type': "application/json"})
    assert response.status_code == 200

def test_mongo_get_book(isbn=418):
    response = requests.request("GET", 'http://localhost:5000/books/{}'.format(isbn))
    assert response.status_code == 200

    data = response.json()
    assert data['isbn'] == isbn

#def test_mongo_update_book(isbn=418):
#    payload ={'price': 406}
#    response = requests.request("PATCH", 'http://localhost:5000/books/{}'.format(isbn), data= payload, headers = {'Content-Type': "application/json"})
#    print(response.status_code)
#    assert response.status_code == 400

#    data = response.json()
#    print(response.json())
#    assert data['isbn'] == isbn

def test_delete_mongo_book(isbn=419):
    response = requests.request("DELETE", 'http://localhost:5000/books/{}'.format(isbn))
    assert response.status_code == 200
