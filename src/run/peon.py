#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Encompasses all application tasks
    TODO: refactor method camel case naming!
"""

from random import choice

from pymongo.errors import OperationFailure
from mongoengine.queryset import DoesNotExist, MultipleObjectsReturned

from src.api.jp.mecab import MeCab
from src.api.jp.wordnet import Wordnet
from src.api.jp.jisho import Jisho
from src.api.language import Language
from src.app.config import languages
from src.db.mongo import connectMongo
from src.db.models import (
    Key,
    Fact,
    Gloss,
    Example,
)


class Peon:

    def __init__(self, db=None):
        if db:
            self.db = db
        else:
            self.db = connectMongo()

    def get(self, id, category='kanji'):
        """Get item by its id and category"""
        " TODO: use objects.get() instead of first"
        return Key.objects(id=id, category='kanji').first()

    def get_item(self, value, category='kanji'):
        """Get item by its id and category"""
        return Key.objects(value=value, category='kanji').first()

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
            # TODO: add fact to item itself!
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
                # TODO: add fact to item itself!
                fact.examples.append(example)
                fact.save()
                results.append((item, fact))

        return results

    def createFact(self, key):
        """ Should create facts, glosses, examples for new items"""
        pass

    def quickLookup(self, key):
        pass

    def process(self, category='kanji', limit=100):
        """Process all new & unprocessed kanji keys"""
        wn = Wordnet()
        mc = MeCab()
        ji = Jisho()
        # 0. Find unprocessed kanji key
        try:
            for key in Key.objects(
                category=category, status='new'
            ).timeout(False).limit(limit):

                print 'Processing ', key.value

                # 0a. Get reading for kanji itself
                key_reading = mc.reading(key.value)
                key_gloss = Gloss()
                key_gloss.readings.update({'default': key_reading})
                key_gloss.save()

                # 0b. Initialize corresponding Fact
                key_fact = Fact(key=key, gloss=key_gloss)

                # 1. Get usages from WordNet
                words = wn.complete(key.value)
                if words:
                    for word in words[:7]:
                        # 2. Check, if reading is found
                        reading = mc.reading(word)
                        if(not reading):
                            continue

                        # 3. Check, if definition is found
                        definitions = wn.lookup(word)
                        if(not definitions):
                            continue

                        # 4. Create new Key and corresponding Fact entities
                        try:
                            # Check if such item already exists
                            existing_key = Key.objects.get(value=word)
                            fact = existing_key.fact
                        except (DoesNotExist, MultipleObjectsReturned):
                            # 5a. Create Gloss entity for most common definitions
                            gloss = Gloss()
                            # No more than 2-4 definitions!
                            for definition in definitions[:3]:
                                gloss.translations.append(definition['gloss'])
                            gloss.readings.update({'default': reading})
                            gloss.save()

                            # 5b. Create corresponding key & fact
                            new_key = Key(
                                value=word,
                                category='word',
                                tags=['minor']
                            ).save()
                            fact = Fact(key=new_key, gloss=gloss).save()
                            new_key.fact = fact
                            new_key.status = 'processed'
                            new_key.save()

                        # TODO: add synonyms based on 'words'?
                        # TODO: parse components?
                        # TODO: find advanced examples?

                        #6. Link fact to key-fact as usages
                        key_fact.usages.append(fact)

                # 1a. If still no usages found
                if len(key_fact.usages) == 0:
                    words = ji.define(key.value, 7)
                    for word, info in words:
                        # 4. Create new Key and corresponding Fact entities
                        try:
                            # Check if such item already exists
                            existing_key = Key.objects.get(value=word)
                            fact = existing_key.fact
                        except (DoesNotExist, MultipleObjectsReturned):
                            # 5a. Create Gloss entity for most common definitions
                            gloss = Gloss()
                            gloss.translations.append(info['meaning'])
                            gloss.readings.update({'default': info['kana']})
                            gloss.save()

                            # 5b. Create corresponding key & fact
                            new_key = Key(
                                value=word,
                                category='word',
                                tags=['minor']
                            ).save()
                            fact = Fact(key=new_key, gloss=gloss).save()
                            new_key.fact = fact
                            new_key.status = 'processed'
                            new_key.save()

                            #6. Link fact to key-fact as usages
                            key_fact.usages.append(fact)

                #7. Save key fact and corresponding key (bi-directional link)
                key_fact.save()
                key.fact = key_fact
                if len(key_fact.usages) > 0:
                    # todo: if still nothing found -> lookup in names
                    # dictionary (jisho)
                    key.status = 'processed'
                key.save()

                print 'Total usages: ', len(key.usages())
                print '----------------'
        except OperationFailure as e:
            print 'There was an error querying mongo db: %s' % e

    def random(self, category='kanji'):
        """Get random item from collection"""
        try:
            return choice(Key.objects(category=category))
        except:
            # No item found in this category
            return Key(value=u'')

    def random_with_usages(self, category='kanji'):
        """
        Get random item, only if some usages provided
        NB: takes some time to compelete due to 'dumb' logic
        """
        # Number of items of such category in DB
        tries = len(Key.objects(category=category))

        while True:
            key = choice(Key.objects(category=category))
            tries -= 1
            if len(key.usages()) > 1 or tries <= 0:
                break

        # No item found in this category
        if tries <= 0:
            return Key(value=u'')
        else:
            return key

    def count(self, category='kanji', status='new'):
        """Count objects by category and status"""
        return len(Key.objects(category=category, status=status))
