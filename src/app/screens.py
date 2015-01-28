#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Application screens
"""

# Additional tools
import json

# Framework
from bottle import (
    route,
    get,
    request,
    jinja2_template as render,
)

# Application modules
from src.db.mongo import connectMongo
from src.db.storage import Storage
from src.run.peon import Peon

from src.api.language import Language
from src.api.jp.weblio import Weblio
from src.api.jp.jisho import Jisho
from src.api.jp.mecab import MeCab

# Initialize MongoDB
db = connectMongo()
# Initialize Redis
store = Storage()


@get('/')
def index():
    """Main page with random kanji"""
    lock = request.get_cookie('lock', secret='secret')
    session = request.environ.get('beaker.session')

    if lock:
        kanji = Peon(db).get(lock)
    else:
        kanji = Peon(db).random()

    favorites = request.get_cookie('favorites', secret='secret')
    fav = False
    if favorites:
        favorites = json.loads(favorites)
        if kanji.value in favorites:
            fav = True

    radicals = store.get_radicals(kanji.value)

    return render(
        'home',
        kanji=kanji,
        radicals=radicals,
        rad_info=store.get_info_for_all(radicals),
        lock=session.get('toggled', False),
        rolled=lock,
        fav=fav,
        single_item=False
    )


@route('/view/:key')
def view_item(key):
    """ View existing kanji """
    kanji = unicode(key, 'utf-8')
    # TODO: test if such item|kanji exists
    radicals = store.get_radicals(kanji)
    session = request.environ.get('beaker.session')
    return render(
        'home',
        kanji=Peon(db).get_item(kanji),
        radicals=radicals,
        rad_info=store.get_info_for_all(radicals),
        lock=session.get('toggled', False),
        single_item=True
    )


@route('/list')
def list_items():
    """ List all items """
    # todo: implement 'view item details on click -> redirect to 'view/%item
    return render('list')


@route('/lookup/:key')
def lookup_item(key):
    """Looks up item definition, translations, readings, examples and so on"""
    # Convert key to unicode
    key = unicode(key, 'utf-8')
    # TODO: profile & move to controller|processor, etc
    # TODO: supported language list (dict?)
    supported = {
        # Single kanji characters may be recognised as Chinese
        'Japanese': set(['ja', 'zh']),
        'English': set(['en']),
        # Some words are nearly identical in Ukrainian
        'Russian': set(['ru', 'uk']),
    }
    # TODO: 'Processor' module to use in scheduler
    # TODO: language detector (in 'Processor'?)
    # Get a set of possible key languages
    detected = set(Language().detect(key))
    # If at least one detected language is supported
    if detected.intersection(supported['Japanese']):
        results = []
        # Get examples
        examples = Weblio().examples(key, 10)
        mecab = MeCab()
        # Get readings for examples
        # TODO: double check, that everything is in unicode
        # TODO: stopped working, check why
        for example, translation in examples.iteritems():
            #reading = mecab.reading(example)
            readings = mecab.wordByWord(example)
            results.append({
                'example': example,
                'readings': readings,
                'translation': translation
            })

        # TODO: add another (optional) key to route -> response type, json|html
        #return {'term': key, 'data': results}

        return render('lookup', term=key, examples=results)

    else:
        return {'result': 'error', 'reason': 'Unsupported language'}


@get('/export')
def export():
    """Exports all favorite kanji in format suitable for anki import"""

    favorites = request.get_cookie('favorites', secret='secret')
    if favorites:
        favorites = json.loads(favorites)
    else:
        favorites = []

    export = {}
    for kanji in favorites:
        details = Jisho().details(kanji),
        if not kanji in details:
            continue
        else:
            details = details[kanji]

        examples = Weblio().examples(kanji)
        example_string = u''
        for example in examples:
            for key, translation in example.iteritems:
                example_string += u'%s: %s <br/>' % (key, translation)

        export[kanji] = {
            'meanings': details['meanings'],
            'readings': u'%s | %s' % (details['kun'], details['on']),
            'examples': example_string
        }

    csv_export = ''
    rows = 4
    for kanji, meta in export.iteritems():
        # Expression, meaning, reading, examples [gloss..]
        csv_export += u"%s\t%s\t%s\t%s\n" % (kanji,
                                           meta['meanings'],
                                           meta['readings'],
                                           meta['examples']
        )

    # result = u"kanji, category\n"
    # kanji_list = Peon(db).export('kanji')
    # for kanji in kanji_list:
    #     result += u"%s, %s\n" % (kanji.value, '0')

    return render('export', export=csv_export, rows=4)


@get('/favs')
def favs():
    """Displays favorite kanji (saved in cookie)"""
    favorites = request.get_cookie('favorites', secret='secret')
    if favorites:
        favorites = json.loads(favorites)
    else:
        favorites = []

    return render('favorites', favorites=favorites)
