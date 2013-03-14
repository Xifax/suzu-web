#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Console tool for suzu-web
'''

from subprocess import call

from argh import (
        arg,
        ArghParser
)

from src.run.peon import Peon

@arg('--limit', default=10, help='How mani new Kanji to add')
def crawl(limit):
    """Launch Scapy spider to crawl web and gather unique kanji"""
    call("cd src; scrapy crawl hebi -a limit=%s" % limit, shell=True)

@arg('--category', default='kanji', help='Item category (e.g., kanji)')
@arg('--limit', default=100, help='Process no more than')
def prepare_usages(category, limit):
    """Generate usages for unprocessed items"""
    peon = Peon()
    peon.process(category, limit)

@arg('category', help='Item category (e.g., kanji)')
def get_random(category):
    """Get random item from db"""
    peon = Peon()
    item = peon.random(category)
    print item.value


if __name__ == '__main__':
    parser = ArghParser()
    parser.add_commands([prepare_usages, get_random, crawl])
    parser.dispatch()

