#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Redis client
"""

import pickle
import os
import chardet

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
        return self

    def prepare_reverse_index(self):
        for kanji, radicals in self.krad.prepare().items():
            for radical in radicals:
                # Assume, that this radical is already in redis
                try:
                    related_kanji = pickle.loads(self.r.get(u'~' + radical))
                    if kanji not in related_kanji:
                        related_kanji.append(kanji)
                        self.r.set(u'~' + radical, pickle.dumps(related_kanji))
                # Otherwise, let's initialize its key
                except (TypeError, IndexError):
                    self.r.set(u'~' + radical, pickle.dumps([kanji]))
        return self

    def prepare_radicals_info(self):
        for radical, fields in self.radicals.prepare().items():
            self.r.set(u'_' + radical, pickle.dumps(fields))
        return self

    def get_radicals(self, kanji):
        """Get radical list for kanji"""
        # Check, if kanji is in db
        if not self.r.exists(kanji):
            # Prepare radicals
            self.prepare_radicals()
        # Get radicals for kanji
        try:
            # todo: should sort radicals by stroke count?
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
            # try to get by alt, if info is empty
            if not info:
                for key in self.r.keys(u'_*'):
                    entry = pickle.loads(self.r.get(key))
                    if rad == entry['alt']:
                        results[rad] = entry
                        break
            else:
                results[rad] = info
        return results

    def find_kanji_with_radical(self, radical, without_reverse_index=False):
        """Find all kanji that are associated with this radical (if any)"""
        if not without_reverse_index:
            try:
                return pickle.loads(self.r.get(u'~' + radical))
            except IndexError:
                return []
        else:
            results = []
            for kanji in self.r.keys('*'):
                if (not kanji.startswith('_') and
                    chardet.detect(kanji)['encoding'] != 'ascii'):
                    try:
                        if radical in pickle.loads(self.r.get(kanji)):
                            results.append(kanji)
                    except IndexError:
                        pass
            return results
