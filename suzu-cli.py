#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Console tool for suzu-web
'''

from argh import *

from src.run.peon import Peon

def prepare_kanji_usages():
    """Generate usages for unprocessed kanji"""
    peon = Peon()
    peon.process()

@arg('category', help='Item category (e.g., kanji)')
def get_random(category):
    """Get random item from db"""
    peon = Peon()
    item = peon.random(category)
    print item.value

if __name__ == '__main__':
    parser = ArghParser()
    parser.add_commands([prepare_kanji_usages, get_random])
    parser.dispatch()

