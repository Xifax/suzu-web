#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Redis client
"""

import pickle
import os

import redis

from src.api.jp.kradfile import Kradfile


class Storage:

    def __init__(self, db=None):
        """ Initialize connection -> either local or Heroku one """
        if not db:
            # Heroku
            try:
                self.r = redis.from_url(
                    os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
                )
            # Local
            except Exception:
                self.r = redis.StrictRedis(host='localhost', port=6379, db=0)
        else:
            self.r = db
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
