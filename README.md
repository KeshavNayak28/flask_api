# flask_api
Flask application to save, update, delete and find data stored in [mongodb](https://docs.mongodb.com/) using api.

You can also use [postman](https://learning.postman.com/docs/postman/api-documentation/documenting-your-api/) to verify ur requests.

Using [Robo-3T](https://robomongo.org/) to check my data stored in Mongo.
## Installation
Commands to install python --version 3+
```bash
sudo apt-get update

sudo apt-get -y install python3.x
```

## Requirement
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Flask and Pymongo
```bash
pip install flask

pip install pymongo
```
You can create a virtual environment and install the required packages with the following commands:
``` bash
$ virtualenv venv

$ . venv/bin/activate

(venv) $ pip install -r requirements.txt
```
## Running The Example
```bash
(venv) $ python3 app.py
```
## Running Using Docker File
To run the main program using Dockerfile pull the code to local system and run the DockerFile using command,
```bash
docker run -d -p 5000:5000 keshav/ubuntu:flask

docker pull mongodb
```
The uri used in mongo connection in database.py is for the mongo image.

For local setup use  uri="mongodb://127.0.0.1:27017"