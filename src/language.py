#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Detect Language API
"""

import requests
from requests import RequestException


class Language:

    def __init__(self):
        self.url = 'http://ws.detectlanguage.com/0.2/detect?q=%s&key=%s'
        self.api_key = 'bb796e6266360e7ce1c633ce56031b9e'

    def detect(self, text):
        """Detect text language code(s)"""
        langs = []
        detected = self.query(text)
        if detected:
            return [
                lang.get('language') for lang
                in detected.get('data').get('detections')
            ]

    def query(self, text):
        """Query Detect Language to determine language(s) code(s)"""
        try:
            return requests.get(
                self.url % (text, self.api_key)
            ).json
        except RequestException:
            return None
