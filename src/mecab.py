#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    MeCab Web API consumer
"""

import requests
from requests import RequestException
from jcconv import kata2hira


class MeCab:
    """
    Queries MeCab Web API (at chasen.org) and returns sentence|word readings
    """

    def __init__(self):
        """Setup request url and default request options"""
        self.url = ('http://chasen.org/~taku/software/mecapi/mecapi.cgi?'
                    'sentence=%s&response=%s&format=json')
        self.options = [
            'surface',          # parts of the sentence
            'feature',          # inflection, baseform, pos
            #'pos',              # part of speech
            #'inflection',       # type and form of inflection
            #'baseform',         # baseform of the word
            'pronounciation'    # word pronounciation
        ]

    def reading(self, sentence, hiragana=True):
        """Get reading for provided sentence|word"""
        info = self.parse(sentence)
        if info:
            kana = u''.join([
                reading.get('pronounciation', '') for reading in info
                if reading.get('pronounciation')
            ])
            if hiragana:
                return kata2hira(kana)
            return kana

    def parse(self, sentence):
        """Query MeCab to parse sentence|word"""
        try:
            return requests.get(
                self.url % (sentence, ','.join(self.options))
            ).json
        except RequestException:
            return None

    def includeReadings(self):
        """nclude reading in response"""
        if 'pronounciation' not in self.options:
            self.options.append('pronounciation')
        return self

    def includeFeature(self):
        """Include feature in response"""
        if 'feature' not in self.options:
            self.options.append('feature')
        return self
