#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Encompasses all application tasks
"""

from random import choice

from src.mecab import MeCab
from src.language import Language
from src.config import languages
from src.models import (
        Key,
        Fact,
        Example
)


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
            # NB: should deinflect to baseform (not so simple, actually!)
            item = Key(value=key, lang=supported.pop())
            if(item.lang == 'Japanese'):
                # Set tags
                item.tags = ['testing']
                # Detect part of speech
                # NB: should probably do this in POST-PROCESSING
                item.pos = MeCab().partOfSpeech(item.value)
                #item.pos, base = MeCab().partOfSpeech(item.value)
                #if base != item.value:
                    #item.value = base
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

    def addItemWithExample(self, key, example):
        """Prepares item, create fact, create example"""
        item = self.addItem(key)
        if item:
            fact = Fact(key=item)
            example = Example(example=unicode(example, 'utf-8')).save()
            fact.examples.append(example)
            fact.save()
            return item, fact, example
        return None

    def addExampleWithItems(self, example, keys):
        """Prepares items, corresponding facts and refereces example"""
        example = Example(example=unicode(example, 'utf-8')).save()
        results = []
        for key in keys:
            item = self.addItem(key)
            if item:
                fact = Fact(key=item)
                fact.examples.append(example)
                fact.save()
                results.append((item, fact))

        return results

    def createFact(self, key):
        """ Should create facts, glosses, examples for new items"""
        pass

    def quickLookup(self, key):
        pass

    def process(self):
        """Process all new & unprocessed keys"""
        pass

    def random(self, category = 'kanji'):
        """Get random item from collection"""
        return choice(Key.objects(category=category))
