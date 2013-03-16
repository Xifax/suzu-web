#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Redis client
"""

import pickle

import redis

from src.api.jp.kradfile import Kradfile


class Storage:

    def __init__(self, redis = None):
        # TODO: Initialize connection -> either local or Heroku one
        # Local
        if not redis:
            self.r = redis.StrictRedis(host='localhost', port=6379, db=0)
        else:
            self.r = redis
        #self.r = redis.from_url('redis://localhost:6379')
        # TODO: Heroku
        self.krad = Kradfile()

    def prepare_radikals(self):
        for kanji, radikals in self.krad.prepare().items():
            # TODO: use setx or setn
            self.r.set(kanji, pickle.dumps(radikals))

    def get_radikals(self, kanji):
        """Get radikal list for kanji"""
        # Check, if radikal are not in db
        if not self.r.exists(kanji):
            # Prepare radikals
            self.prepare_radikals()
        # Get radikals for kanji
        return pickle.loads(self.r.get(kanji))

if __name__ == '__main__':
    red = Storage()
    for rad in red.get_radikals(u'語'):
        print rad
