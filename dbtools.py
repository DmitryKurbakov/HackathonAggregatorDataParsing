from mongoengine import *
from sshtunnel import SSHTunnelForwarder
import googlemaps
import re
import api
import pymongo
from pymongo import errors
import time
import urllib
from bs4 import BeautifulSoup
import urllib.request

server = SSHTunnelForwarder(
    api.MONGO_HOST,
    ssh_username=api.MONGO_USER,
    ssh_password=api.MONGO_PASS,
    remote_bind_address=('localhost', 27017)
)

server.start()

connect(
    db=api.MONGO_DB,
    host='localhost',
    port=server.local_bind_port
)


class Source(Document):

    title = StringField(required=True)
    location = StringField()
    preview = StringField()
    time = StringField()
    ref = StringField()
    area = ListField()
    source = StringField()
    geocode = StringField()


def insert_data(data):

    client = pymongo.MongoClient('localhost', server.local_bind_port)  # server.local_bind_port is assigned local port
    db = client[api.MONGO_DB]

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
                          area=[],
                          source=data[i].source,
                          geocode="")
            temp.save()
        i = i + 1


def set_geocode():

    client = pymongo.MongoClient('localhost', server.local_bind_port)  # server.local_bind_port is assigned local port
    db = client[api.MONGO_DB]

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


def get_text_for_type_definition():
    t0 = time.time()

    client = pymongo.MongoClient('localhost', server.local_bind_port)  # server.local_bind_port is assigned local port
    db = client[api.MONGO_DB]
    sources = db.source

    text = []
    cursor = sources.find({})
    i = 0
    for doc in cursor:
        # if i == 10:
        #     break
        url = doc.get('ref')
        try:
            temp = doc.get("area")
            if len(temp) == 0:
                page = urllib.request.urlopen(url).read()
                soup = BeautifulSoup(page)

                text.append(
                    {
                        'text': '{} {} {}'.format(doc.get('title'), doc.get('preview'), soup.text).lower(),
                        'id': doc.get("_id")
                    })
                print(str(i) + ':\t' + 'get_text_for_type_definition-url: ' + url + '\tok')
        except:
            print(url + '\tfail')
            text.append(
                {
                    'text': '{} {}'.format(doc.get('title'), doc.get('preview')).lower(),
                    'id': doc.get("_id")
                })
            continue
        i += 1
    t1 = time.time()

    print('get_text_for_type_definition: {}'.format(str(t1 - t0)))
    return text


def set_areas_for_document(id, areas):
    try:
        client = pymongo.MongoClient('localhost', server.local_bind_port)  # server.local_bind_port is assigned local port
        db = client[api.MONGO_DB]
        sources = db.source

        print('areas for id: {} are: {}\ntransferred to database'.format(id, areas))
        sources.update({"_id": id}, {"$set": {'area': areas}})
    except pymongo.errors.AutoReconnect:
        print('Mongo reconnect...')
        time.sleep(30)
        server.restart()

def get_type_and_keywords():
    client = pymongo.MongoClient('localhost', server.local_bind_port)  # server.local_bind_port is assigned local port
    db = client[api.MONGO_DB]
    db_types = db.types

    types = []
    keywords = []

    doc = db_types.find({})

    for it in doc:
        print("Types from database: " + str(it.keys()))
        types = list(it.keys())
        types.remove('_id')

        for t in types:
            keywords.append(it.get(t))
    i = 0
    return {
        'types': types, 'keywords': keywords
    }