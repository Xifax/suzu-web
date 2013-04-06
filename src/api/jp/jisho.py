#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Jisho.org semi-api
"""

import requests
from requests import RequestException
from bs4 import BeautifulSoup


class Jisho:

    def __init__(self):
        self.url = u'http://jisho.org/words?jap=%s&eng=&dict=edict'

    def lookup(self, term):
        """Lookup term on jisho"""
        try:
            return requests.get(self.url % term).content
        except RequestException:
            return ''
    
    def complete(self, kanji):
        """Get words which include specified kanji"""
        results = []
        soup = BeautifulSoup(self.lookup(kanji), 'lxml')
        for word in soup.find_all('span', {'class': 'kanji'}):
            # get text from html element, strip spaces and tabs
            word = word.get_text().strip()
            # skip kanji itself
            if word != kanji:
                results.append(word)
                
        return results
        
    def define(self, kanji):
        """Get words with specified kanji + translations"""
        pass
    
if __name__ == '__main__':
    for word in Jisho().complete(u'鍵'):
        print word