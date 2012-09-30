#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Weblio API(as if) consumer
'''

import requests
from requests import RequestException
from bs4 import BeautifulSoup


class Weblio:

    def __init__(self):
        self.definition_url = 'http://www.weblio.jp/content/%s'
        self.lookup_url = 'http://ejje.weblio.jp/content/%s'
        self.examples_url = 'http://ejje.weblio.jp/sentence/content/%s'
        # TODO: stats

    def definition(self, term):
        '''Fetches definitions and similar words'''
        data = self.process(self.definition_url, term)
        if data:
            # Check for different possible divs:
            # NetDicBody
            # Wiktionary
            gloss = data.find('div', 'NetDicBody')
            #print gloss.getText()
            definitions = gloss.getText().split('(')
            print definitions

    def lookup(self, term):
        '''Fetches translations (jp-en) for different use-cases'''
        pass

    def examples(self, term):
        '''Fetches examples'''
        data = self.process(self.examples_url, term)
        if data:
            for example in data.find_all('div', 'qotC')[:2]:
                print example.contents[0].getText()
                source = example.contents[1].span.getText()
                print example.contents[1].getText().replace(source, '')

    def process(self, url, term):
        try:
            return BeautifulSoup(requests.get(url % term).text)
        except RequestException:
            return None


if __name__ == '__main__':
    '''Run as test script'''
    #term = u'募らす'
    term = u'読み方'
    '''
    r = requests.get('http://ejje.weblio.jp/sentence/content/%s' % term)
    data = BeautifulSoup(r.text)
    # Two examples should be plenty | TODO: get random two indices?
    for example in data.find_all('div', 'qotC')[:2]:
        # Sentence
        print example.contents[0].getText()
        # Translation
        source = example.contents[1].span.getText()
        print example.contents[1].getText().replace(source, '')
    '''

    weblio = Weblio()
    weblio.definition(term)
    #weblio.examples(term)
