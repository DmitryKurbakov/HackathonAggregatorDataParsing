from mongoengine import *
from sshtunnel import SSHTunnelForwarder
import googlemaps
import re
import api
import pymongo


MONGO_HOST = "185.235.129.54"
MONGO_DB = "HackathonAggregator"
MONGO_USER = "root"
MONGO_PASS = "Ucb4GJxmv5Pr"

server = SSHTunnelForwarder(
    MONGO_HOST,
    ssh_username=MONGO_USER,
    ssh_password=MONGO_PASS,
    remote_bind_address=('localhost', 27017)
)

server.start()

connect(
    db=MONGO_DB,
    host='localhost',
    port=server.local_bind_port
)

class Source(Document):

    title = StringField(required=True)
    location = StringField()
    preview = StringField()
    time = StringField()
    ref = StringField()
    area = StringField()
    source = StringField()
    geocode = StringField()


def insert_data(data):

    server.start()
    client = pymongo.MongoClient('localhost', server.local_bind_port)  # server.local_bind_port is assigned local port
    db = client[MONGO_DB]

    sources = db.source

    i = 0

    while i<len(data):

        f = sources.find_one({"title": data[i].title})
        if not f:
            temp = Source(title=data[i].title,
                          location=data[i].location,
                          preview=data[i].preview,
                          time=data[i].time,
                          ref=data[i].ref,
                          area=data[i].area,
                          source=data[i].source,
                          geocode="")
            temp.save()
        i = i + 1

def set_geocode():

    server.start()

    client = pymongo.MongoClient('localhost', server.local_bind_port)  # server.local_bind_port is assigned local port
    db = client[MONGO_DB]

    sources = db.source

    gmaps = googlemaps.Client(key=api.gkey)

    cursor = sources.find({})
    for doc in cursor:
        if not doc.get("geocode"):
            sources.update({"_id": doc.get("_id")}, {"$set": {'geocode': ""}})
        try:
            temp = doc.get("location")
            if temp != "" and (doc.get('geocode') == 1.0 or doc.get('geocode') == ""):

                geo = gmaps.geocode(re.sub(r'\s+', ' ', doc.get("location")))

                print(geo)
                sources.update({"_id": doc.get("_id")}, {"$set": {'geocode': geo}})
        except:
            continue

    server.stop()

