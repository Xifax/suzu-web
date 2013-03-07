#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Encompasses all application tasks
"""

from random import choice

from src.api.jp.mecab import MeCab
from src.api.jp.wordnet import Wordnet
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
        return Key.objects(id=id, category='kanji').first()

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

    def process(self, category = 'kanji'):
        """Process all new & unprocessed kanji keys"""
        wn = Wordnet()
        mc = MeCab()
        # 0. Find unprocessed kanji key
        for key in Key.objects(category=category, status='new'):

            print 'Processing ', key.value

            # 0a. Get reading for kanji itself
            key_reading = mc.reading(key.value)
            key_gloss = Gloss()
            key_gloss.readings.update({'default': key_reading})
            key_gloss.save()

            # 0b. Initialize corresponding Fact
            key_fact = Fact(key=key, gloss=key_gloss)


            # TODO: If no words found -> lookup in weblio?
            # eg: http://www.weblio.jp/content_find/contains/0/%E6%AA%8E

            # 1. Complete kanji with words-compounds-usages from WordNet
            # No more than 3-10 usages!
            # TODO: preferably semi-random!
            for word in wn.complete(key.value)[:7]:
                # 2. Check, if reading is found
                reading = mc.reading(word)
                if(not reading):
                    continue

                # 3. Check, if definition is found
                definitions = wn.lookup(word)
                if(not definitions):
                    continue

                # 4. Create Gloss entity for most common definitions
                #definition = definitions.pop()
                gloss = Gloss()
                # No more than 2-4 definitions!
                for definition in definitions[:3]:
                    gloss.translations.append(definition['gloss'])
                gloss.readings.update({'default': reading})
                gloss.save()

                # 5. Create new Key and corresponding Fact entities
                new_key = Key(value=word, category='word', tags=['minor']).save()
                fact = Fact(key=new_key, gloss=gloss).save()
                new_key.fact = fact
                new_key.status = 'processed'
                new_key.save()

                # TODO: add synonyms based on 'words'?
                # TODO: parse components?
                # TODO: find advanced examples?

                #6. Link fact to key-fact as usages
                key_fact.usages.append(fact)

            #7. Save key fact and corresponding key (bi-directional link)
            key_fact.save()
            key.fact = key_fact
            key.status = 'processed'
            key.save()

            print 'Total usages: ', len(key.usages())
            print '----------------'

    def random(self, category = 'kanji'):
        """Get random item from collection"""
        try:
            return choice(Key.objects(category=category))
        except:
            # No item found in this category
            return Key(value=u'')

