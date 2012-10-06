#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Encompasses all application tasks
"""

from src.mecab import MeCab
from src.language import Language
from src.config import languages
from src.models import Key

# Initialize MongoDB
# TODO: move to init
#db = Mongo(db='facts', host='127.0.0.1', port=27818)
#db = Mongo(db='facts')
#db.connect()
#db = MongoOnHeroku('facts')
#db = MongoOnHeroku('app3405448')


class Peon:

    def __init__(self, db=None):
        if db:
            # NB: actully, if it's connected, it should work
            self.db = db
        else:
            # TODO: initialize|connect
            pass

    def addItem(self, key):
        """Add pending item to DB"""
        key = unicode(key, 'utf-8')
        # Check, if key already exists
        if len(Key.objects(value=key)) == 1:
            return None

        # Detect language
        detected = set(Language().detect(key))
        supported = [
            lang for lang in languages
            if detected.intersection(languages.get(lang))
        ]
        # Supported language detected
        if supported:
            item = Key(value=key, lang=supported.pop())
            # TODO: process based on language
            if(item.lang == 'Japanese'):
                # Set tags
                item.tags = ['testing']
                # Detect part of speech
                # NB: should probably do this in POST-PROCESSING
                item.pos = MeCab().partOfSpeech(item.value)
                # TODO: get type (somehow, based on pos)
                # TODO: if noun & 1 symbol == kanji, if two and more = word...
                if len(item.value) == 1:
                    item.category = 'kanji'
                elif item.pos == '':
                    item.category = 'compound'
                else:
                    item.category = 'word'
            # Unprocesed item
            item.status = 'new'
            # Save item
            item.save()
            return item
        # Unsupported language
        else:
            return None

    def createFact(self, key):
        """ Should create facts, glosses, examples for new items"""
        pass

    def quickLookup(self, key):
        pass

    def process(self):
        """Process all new & unprocessed keys"""
        pass
