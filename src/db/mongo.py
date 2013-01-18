#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    DB connection handler and tools
"""

import os

from mongoengine import connect


class Mongo():

    def __init__(self, db, uri=None, host='localhost', port=27017):
        """Initialize MongoDB handler"""
        self.db = db
        self.uri = uri
        self.host = host
        self.port = port

    def connect(self):
        """Connect to MongoDB"""
        if(self.uri):
            connect(self.db, self.uri)
        else:
            connect(self.db, host=self.host, port=self.port)


class MongoOnHeroku(Mongo):

    def __init__(self, db=None):
        """Initialize MongoDB on Heroku"""
        if not db:
            db = os.environ['MONGOHQ_URL'].split('/')[1]
        connect(db, host=os.environ['MONGOHQ_URL'])


def connectMongo():
    """Try to connect to either development or production DB"""
    try:
        # By default use production DB on Heroku
        db = MongoOnHeroku()
    except Exception:
        # If could not connect, try development mongo DB
        db = Mongo(db='facts')
        db.connect()

    return db
