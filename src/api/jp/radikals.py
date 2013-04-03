#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Prepare radikals info
"""

import requests
from requests import RequestException
from bs4 import BeautifulSoup


class Radikals:

    def __init__(self):
        self.url = 'https://docs.google.com/spreadsheet/ccc?key=0AqYInAMvWw-2cmxGbkZNUWpYcmZTZlVVY0xJbU9tVlE&hl=en#gid=0'

    def get_radikals_info(self):
        """Get info"""
        try:
            return requests.get(self.url).content
        except RequestException:
            return ''

    def prepare(self):
        """Parse radikals info into dictionary"""
        results = {}

        # Parse resulting table
        info = self.get_radikals_info()
        soup = BeautifulSoup(info, 'lxml')
        rows = soup.find_all('tr')
        # Prepare dictionary entry for each row
        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 8:
                radikal = cells[3].get_text()
                if radikal:
                    results[radikal] = {
                        # Alternative radikal
                        'alt':          cells[4].get_text() if cells[4] else '',
                        # Number of strokes
                        'strokes':      cells[5].get_text(),
                        # Japanese name
                        'name':         cells[6].get_text(),
                        # Primitive name (RTK, english)
                        'primitive':    cells[7].get_text(),
                    }

        return results


if __name__ == '__main__':
    results = Radikals().prepare()
    print len(results)
    import pprint
    pprint.pprint(results)
