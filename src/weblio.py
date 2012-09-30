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
        #self.definition_url = 'http://www.weblio.jp/content/%s'
        # Cannot find some rare words
        self.definition_url = 'http://ejje.weblio.jp/english-thesaurus/%s'
        self.lookup_url = 'http://ejje.weblio.jp/content/%s'
        self.examples_url = 'http://ejje.weblio.jp/sentence/content/%s'
        # TODO: stats

    def definition(self, term):
        '''Fetches definitions and similar words, synonyms'''
        data = self.process(self.definition_url, term)
        # TODO: implement!
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
        examples = []
        if data:
            # Iterate from the END, not the beginning
            for example in data.find_all('div', 'qotC')[2:]:
                # TODO: if no examples found -> log it (and mark term)
                # TODO: check (term:example) when there's english example [0] instead
                print example.contents[0].getText()
                source = example.contents[1].span.getText()
                print example.contents[1].getText().replace(source, '')


                # temporary solution
                #examples.append(example.contents[0].getText())

        return examples

    def process(self, url, term):
        try:
            return BeautifulSoup(requests.get(url % term).text)
        except RequestException:
            return None


def local_run():
    output = open('/home/yadavito/Desktop/test2_export.txt', 'w')
    export = []
    for line in open('/home/yadavito/Desktop/test2.txt'):
        fields = line.split('\t')
        term = fields[0]
        weblio = Weblio()
        examples = weblio.examples(term)
        if examples:
            example = weblio.examples(term).pop()
        else:
            example = u''
        #print example
        fields[0] = unicode(fields[0], 'utf-8')
        fields[1] = unicode(fields[1], 'utf-8')
        fields[2] = unicode(fields[2], 'utf-8')
        fields[3] = example
        export.append(fields)

    print export
    for line in export:
        output.write(u'\t'.join(line).encode('utf-8'))
        # OMG
        output.write('\n')

if __name__ == '__main__':
    '''Run as test script'''
    #term = u'募らす'
    term = u'読み方'
    '''
    r = requests.get('http://ejje.weblio.jp/sentence/content/%s' % term)
    data = BeautifulSoup(r.text)
    # Two examples should be plenty | TODO: get random two indices?
    for example in data.find_all('div', 'qotC')[2:]:
        # Sentence
        print example.contents[0].getText()
        # Translation
        source = example.contents[1].span.getText()
        print example.contents[1].getText().replace(source, '')
    '''

    #weblio = Weblio()
    #weblio.definition(term)
    #weblio.examples(term)
    local_run()

