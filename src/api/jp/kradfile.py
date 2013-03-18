#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Kradfile-u consumer
"""

import requests
from requests import RequestException


class Kradfile:

    def __init__(self):
        self.url = 'http://www.kanjicafe.com/downloads/kradfile-u.gz'

    def get_kradfile(self):
        """Get Kradfile-u"""
        try:
            return requests.get(self.url).content
        except RequestException:
            return ''

    def prepare(self):
        """Parse Kradfile into dictionary"""
        results = {}
        for line in self.get_kradfile().split('\n'):
            if not line or line.startswith('#'):
                continue

            kanji, radikals = line.split(':')
            results[kanji.strip()] = [
                unicode(rad, 'utf-8') for rad
                in radikals.split(' ')
                if rad != ''
            ]

        return results


if __name__ == '__main__':
    results = Kradfile().prepare()
    print len(results)
    print results.popitem()
