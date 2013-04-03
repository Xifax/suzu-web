#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Redis client
"""

import pickle
import os

import redis

from src.api.jp.kradfile import Kradfile
from src.api.jp.radikals import Radikals


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
        self.radikals = Radikals()

    def prepare_radikals(self):
        for kanji, radikals in self.krad.prepare().items():
            # TODO: use setx or setn
            self.r.set(kanji, pickle.dumps(radikals))

    def prepare_radikals_info(self):
        for radikal, fields in self.radikals.prepare().items():
            self.r.set(u'_' + radikal, pickle.dumps(fields))

    def get_radikals(self, kanji):
        """Get radikal list for kanji"""
        # Check, if kanji is in db
        if not self.r.exists(kanji):
            # Prepare radikals
            self.prepare_radikals()
        # Get radikals for kanji
        try:
            return pickle.loads(self.r.get(kanji))
        except TypeError:
            return []

    def get_radikal_info(self, radikal):
        """Get information about radikal"""
        # Get radikal info
        try:
            return pickle.loads(self.r.get(u'_' + radikal))
        except TypeError:
            return []

    def get_info_for_all(self, radikals):
        """Get information for all of the radikals"""
        results = {}
        for rad in radikals:
            results[rad] = self.get_radikal_info(rad)
        return results
