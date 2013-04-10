#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Jisho.org semi-api
"""

import re
from collections import OrderedDict
from itertools import islice

import requests
from requests import RequestException
from bs4 import BeautifulSoup


class Jisho:

    def __init__(self):
        # Starting with
        self.url = u'http://jisho.org/words?jap=%s&eng=&dict=edict'
        # Any position
        self.fuzzy_url = u'http://jisho.org/words?jap=*%s*&eng=&dict=edict'
        # Details
        self.details_url = u'http://jisho.org/kanji/details/%s'

    def lookup(self, term, fuzzy=True):
        """Lookup term on Jisho"""
        url = self.fuzzy_url if fuzzy else self.url
        try:
            return requests.get(url % term).content
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

    def define(self,
               kanji,
               limit=20,
               skip_same_reading=False,
               skip_same_meaning=False):
        """Get words with specified kanji + meaning + kana
        Returns iterator.
        """
        results = OrderedDict({})

        soup = BeautifulSoup(self.lookup(kanji), 'lxml')

        # Utility function to get specific row|column text
        get_row = lambda row, column: row.find('td', column).get_text().strip()
        columns = ['kanji_column', 'kana_column', 'meanings_column']

        # Find rows with classes 'odd' and 'even'
        for row in soup.find_all("tr", {"class": re.compile(r"^(odd|even)$")}):
            # Skip 'lower' classes
            if 'lower' in row['class']:
                continue

            # Get columns by names
            word, kana, meaning = [get_row(row, column) for column in columns]

            # Append to results if not the same kanji
            if word != kanji:
                results[word] = {'kana': kana, 'meaning': meaning}

        # todo: filter results based on flags
        # todo: may filter by the same meaning and kana

        return islice(results.iteritems(), limit)

    def details(self, word):
        """Get info for each kanji in word"""
        details = {}
        try:
            data = BeautifulSoup(
                requests.get(self.details_url % word).content, 'lxml'
            )

            for div in data.find_all('div', 'kanji_result'):

                # Get kanji, its meanings and readings
                kanji = div.find('h1', 'literal').get_text().strip()
                meanings = div.find('div', 'english_meanings') \
                    .get_text(strip=True).replace('English meanings', '')
                try:
                    kun, on = div.find('div', 'japanese_readings') \
                        .get_text().strip().split('\n')
                    names = u''
                except ValueError:
                    kun, on, names = div.find('div', 'japanese_readings') \
                        .get_text().strip().split('\n')

                details[kanji] = {
                    'meanings': meanings.replace(';', ', '),
                    'on': on.replace('Japanese on:', '').strip(),
                    'kun': kun.replace('Japanese kun:', '').strip(),
                    'names': names.replace('Japanese names:', '').strip()
                }
        except RequestException:
            pass

        return details


if __name__ == '__main__':
    for item, value in Jisho().details(u'才凱旋').iteritems():
        print item
        for key, data in value.iteritems():
            print key, data
