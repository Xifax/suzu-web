#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Prepare radicals info
"""

import requests
from requests import RequestException
from bs4 import BeautifulSoup


class Radicals:

    def __init__(self):
        # public spreadsheet with base radicals collection
        # TODO: some of the radicals are missing! Gonna catch'em all
        self.url = ('https://docs.google.com/spreadsheet/ccc?'
                    'key=0AkI3jF0lqjOLdGZobEV0bHNHRW1MSmF6dnd6TGh6c3c#gid=0')

    def get_radicals_info(self):
        """Get info"""
        try:
            return requests.get(self.url).content
        except RequestException:
            return ''

    def prepare(self):
        """Parse radicals info into dictionary"""
        results = {}

        # Parse resulting table
        info = self.get_radicals_info()
        soup = BeautifulSoup(info, 'lxml')
        rows = soup.find_all('tr')
        # Prepare dictionary entry for each row
        for row in rows:
            cells = row.find_all('td')
            # Total number of columns, including bogus one
            if len(cells) == 7:
                radical = cells[1].get_text()
                if radical:
                    results[radical] = {
                        # Alternative radical
                        'alt':          cells[2].get_text() if cells[2] else '',
                        # Number of strokes
                        'strokes':      cells[3].get_text(),
                        # Japanese name
                        'name':         cells[4].get_text(),
                        # Primitive name (RTK, english)
                        'primitive':    cells[5].get_text(),
                    }

        return results
