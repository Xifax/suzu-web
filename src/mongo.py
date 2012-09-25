#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    DB connection handler and tools
'''

import os

from mongoengine import connect


class Mongo():

    def __init__(self, db, uri=None, host='localhost', port=27017):
        '''Initialize MongoDB handler'''
        self.db = db
        self.uri = uri
        self.host = host
        self.port = port

    def connect(self):
        '''Connect to MongoDB'''
        if(self.uri):
            connect(self.db, self.uri)
        else:
            connect(self.db, host=self.host, port=self.port)


class MongoOnHeroku(Mongo):

    def __init__(self, db):
        '''Initialize MongoDB on Heroku'''
        super(self, db=db, uri=os.environ['MONGO_URL'])
        self.connect()
