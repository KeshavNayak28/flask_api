FROM ubuntu
RUN apt-get update
RUN apt-get -y install python3
RUN apt-get install -y python3-pip
RUN pip3 install flask
RUN pip3 install pymongo
RUN mkdir /ss
WORKDIR /ss
COPY . .
EXPOSE 5000
CMD python3 app.py