#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Console tool for suzu-web
'''

from argh import ArghParser

from src.run.cli import *


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
