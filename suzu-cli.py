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
from src.db.storage import Storage


def prepare_radikals():
    """Prepare radikal decomposition data"""
    Storage().prepare_radikals()


@arg('kanji', help='Kanji to lookup')
def get_radikals(kanji):
    """Get radikal decomposition for provided kanji"""
    for rad in Storage().get_radikals(kanji):
        print rad


@arg('--limit', default=10, help='How mani new Kanji to add')
def crawl(limit):
    """Launch Scapy spider to crawl web and gather unique kanji"""
    call("PATH=$PATH:$HOME/bin")
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
    parser.add_commands([
        prepare_usages, prepare_radikals, get_random, get_radikals, crawl
    ])
    parser.dispatch()
