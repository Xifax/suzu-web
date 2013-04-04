#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Redis client
"""

import pickle
import os

import redis

from src.api.jp.kradfile import Kradfile
from src.api.jp.radicals import Radicals


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
        self.radicals = Radicals()

    def prepare_radicals(self):
        for kanji, radicals in self.krad.prepare().items():
            # TODO: use setx or setn
            self.r.set(kanji, pickle.dumps(radicals))

    def prepare_radicals_info(self):
        for radical, fields in self.radicals.prepare().items():
            self.r.set(u'_' + radical, pickle.dumps(fields))

    def get_radicals(self, kanji):
        """Get radical list for kanji"""
        # Check, if kanji is in db
        if not self.r.exists(kanji):
            # Prepare radicals
            self.prepare_radicals()
        # Get radicals for kanji
        try:
            return pickle.loads(self.r.get(kanji))
        except TypeError:
            return []

    def get_radical_info(self, radical):
        """Get information about radical"""
        # Get radical info
        try:
            return pickle.loads(self.r.get(u'_' + radical))
        except TypeError:
            return []

    def get_info_for_all(self, radicals):
        """Get information for all of the radicals"""
        results = {}
        for rad in radicals:
            info = self.get_radical_info(rad)
            # try to get by alias, if info is empty
            if not info:
                # scan all _keys to get, unserialize and find alias?
                for key in self.r.keys(u'_*'):
                    entry = pickle.loads(self.r.get(key))
                    if rad == entry['alt']:
                        results[rad] = entry
                        break
                # todo: log this radical?
                # todo: ponder, what to do with strange radicals
            else:
                results[rad] = info
        return results
