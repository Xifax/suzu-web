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


def prepare_radicals():
    """Prepare radical decomposition data"""
    Storage().prepare_radicals() \
        .prepare_radicals_info() \
        .prepare_reverse_index()


@arg('kanji', help='Kanji to lookup')
def get_radicals(kanji):
    """Get radical decomposition for provided kanji"""
    for rad in Storage().get_radicals(kanji):
        print rad


@arg('--limit', default=10, help='How mani new Kanji to add')
def crawl(limit):
    """Launch Scapy spider to crawl web and gather unique kanji"""
    #call('export PATH=$PATH:$HOME/bin')
    call("cd src; scrapy crawl hebi -a limit=%s" % limit, shell=True)


@arg('--category', default='kanji', help='Item category (e.g., kanji)')
@arg('--limit', default=100, help='Process no more than')
def prepare_usages(category, limit):
    """Generate usages for unprocessed items"""
    Peon().process(category, limit)


@arg('--category', default='kanji', help='Item category (e.g., kanji)')
@arg('--with-usages', default=False, help='Get items with usages')
def get_random(args):
    """Get random item from db"""
    peon = Peon()
    if not args.with_usages:
        item = peon.random(args.category)
    else:
        item = peon.random_with_usages(args.category)
    print item.value, '\nUsages:'
    for usage in item.usages():
        print usage.value()


@arg('--category', default='kanji', help='Item category (e.g., kanji)')
def count_new(category):
    """Count unprocessed items"""
    print Peon().count(category, 'new')


if __name__ == '__main__':
    parser = ArghParser()
    parser.add_commands([
        prepare_usages,
        prepare_radicals,
        get_random,
        get_radicals,
        crawl,
        count_new,
    ])
    parser.dispatch()
