# from pymongo import MongoClient
#
#
#
# def insert(rows):
#     client = MongoClient()
#
#     db = client.HackathonAggregator
#     sources = db.Sources
#
#     for row in rows:
#         sources.insert_one(row.title).inserted_id
#         sources.insert_one(row.location).inserted_id
#         sources.insert_one(row.preview).inserted_id
#         sources.insert_one(row.description).inserted_id
#         sources.insert_one(row.time).inserted_id

from mongoengine import *
from pymongo import MongoClient

connect('HackathonAggregator')


class Source(Document):
    title = StringField(required=True)
    location = StringField()
    preview = StringField()
    description = StringField()
    time = StringField()
    ref = URLField()


def insert_data(data):
    client = MongoClient()

    db = client.HackathonAggregator
    sources = db.source

    i = 0

    while i<len(data):

        if not sources.find_one({"title": data[i].title}):
            temp = Source(title=data[i].title,
                          location=data[i].location,
                          preview=data[i].preview,
                          description=data[i].description,
                          time=data[i].time,
                          ref=data[i].ref)
            temp.save()
        i = i + 1
