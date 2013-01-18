#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    DB entities
"""

from datetime import datetime

from mongoengine import (
    Document,
    StringField,
    IntField,
    ListField,
    DictField,
    ReferenceField,
    DateTimeField,
)


class Key(Document):
    """Fact key"""
    # Key value
    value = StringField()
    # Corresponding fact
    fact = ReferenceField('Fact')
    # Corresponding tags
    tags = ListField()
    # Language (consider it special tag)
    lang = StringField()
    # Type (kanji, word, word pair, idiom)
    category = StringField()
    # Part of speech
    pos = StringField()
    # Processing status
    status = StringField(default='new')
    # Date added
    added = DateTimeField(default=datetime.today())
    # Times exported
    exported = IntField(default=0)


class Gloss(Document):
    """Fact glossary"""
    # Thesaurus definitions (in native language)
    definitions = ListField()
    # Possible readings with different types
    readings = DictField()
    # Translations (independent from definitions)
    translations = ListField()


class Example(Document):
    """Relatively complex usage example"""
    # Example
    example = StringField()
    # Translation
    translation = StringField()


class Fact(Document):
    """Simple lexical term: kanji, word, idiom and so on"""
    # Key (uid, search index)
    key = ReferenceField('Key')
    # Glossary (reading, definition, translation, etc)
    gloss = ReferenceField('Gloss')

    # Components (list of kanji, words, radikals and so on)
    components = DictField()
    # Complex usage examples (sentences)
    examples = ListField(ReferenceField('Example'))
    # Simple usage examples (word pairs, compounds, idioms)
    usages = ListField(ReferenceField('self'))

    # Synonyms (similar meaning)
    synonyms = ListField(ReferenceField('self'))
    # Antonyms (opposite meaning)
    antonyms = ListField(ReferenceField('self'))
    # Homonyms (different meaning, same pronounsation)
    homonyms = ListField(ReferenceField('self'))
    # Omonyms (different meaning, same pronounsation and written form)
    omonyms = ListField(ReferenceField('self'))


class Stats(Document):
    """Request stats, traffic stats, failure stats and so on"""
    # Name of the module
    name = StringField()
    # Requests count
    requests = IntField(default=0)
    # Request time (in ms)
    time = IntField(default=0)
    # Number of failures
    failures = IntField(default=0)
    # Failure logs [time: failure info]
    logs = DictField()
    # Specific info
    info = DictField()