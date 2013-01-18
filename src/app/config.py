#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Application config
"""

# Supported languages
languages = {
    # Single kanji characters may be recognised as Chinese
    'Japanese': set(['ja', 'zh']),
    'English': set(['en']),
    # Some words are nearly identical in Ukrainian
    'Russian': set(['ru', 'uk']),
}

# Keys types
categories = [
    'kanji',
    'word',
    'word pair',
    'compound',
    'idiom',
    'sentence',
]

# Keys statuses
statuses = [
    'new',
    'processed',
    'failure',
]
