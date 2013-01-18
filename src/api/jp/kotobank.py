#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Kotobank API(not so much) consumer
"""

import requests
from requests import RequestException
from bs4 import BeautifulSoup

class Kotobank:

    def __init__(self):
        self.url = 'http://kotobank.jp/word/%'

    def lookup(self, word):
        """Used to lookup word definitions as jp-jp"""
