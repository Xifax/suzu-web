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

def crawl():
    """Launch Scapy spider to crawl web and gather unique kanji"""
    call("cd src; scrapy runspider hebi/spiders/spider.py", shell=True)
    #call("PATH=$PATH:$HOME/bin")
    #call("cd src; ../bin/scrapy runspider hebi/spiders/spider.py", shell=True)

@arg('category', help='Item category (e.g., kanji)')
def prepare_usages(category):
    """Generate usages for unprocessed items"""
    peon = Peon()
    peon.process(category)

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

