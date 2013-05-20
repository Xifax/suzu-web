#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Imports
###############################################################################

# Stdlib
import os

# Framework modules
import bottle
import bottle_werkzeug
from bottle import (
    request,
    response,
    get,
    route,
    static_file,
    error,
    jinja2_template as render,
)

# Application modules
from src.db.models import Key
from src.db.mongo import connectMongo
from src.db.storage import Storage

from src.api.language import Language
from src.api.jp.weblio import Weblio
from src.api.jp.mecab import MeCab
from src.run.peon import Peon

###############################################################################
# Initializing framework, DB connection and paths
###############################################################################

# Initialize Werkzeug plugin
wz = bottle_werkzeug.Plugin(evalex=True)  # should work without True
bottle.install(wz)
# Enable debug mode
bottle.debug(True)
# Process request by Werkzeug
req = wz.request

# Initialize MongoDB
db = connectMongo()
# Initialize Redis
store = Storage()


###############################################################################
# Separate pages
###############################################################################


@get('/')
def index():
    """Main page with random kanji"""
    lock = request.get_cookie('lock', secret='secret')
    session = request.environ.get('beaker.session')

    if lock:
        kanji = Peon(db).get(lock)
    else:
        kanji = Peon(db).random()

    radicals = store.get_radicals(kanji.value)

    return render(
        'home',
        kanji=kanji,
        radicals=radicals,
        rad_info=store.get_info_for_all(radicals),
        lock=session.get('toggled', False)
    )


@route('/view/:key')
def view_item(key):
    """ View existing kanji """
    kanji = unicode(key, 'utf-8')
    # TODO: test if such kanji exists
    radicals = store.get_radicals(kanji)
    session = request.environ.get('beaker.session')
    return render(
        'home',
        kanji=Peon(db).get_item(kanji),
        radicals=radicals,
        rad_info=store.get_info_for_all(radicals),
        lock=session.get('toggled', False)
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
        for example, translation in examples:
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


###############################################################################
# Api calls
###############################################################################


@route('/add/:key')
def add_item(key):
    """Add new item"""
    if Peon(db).addItem(key):
        return {'result': 'success'}
    else:
        return {'result': 'failure', 'reason': 'Item is already in DB'}


@route('/del/:key')
def del_item(key):
    """Remove existing item"""
    results = {}
    for item in Key.objects(value=key):
        item.delete()
        results[key] = {'result': 'success'}
    return results


@route('/add/:key/:example')
def add_item_with_example(key, example):
    """Add new item, generate fact and link example"""
    if Peon(db).addItemWithExample(key, example):
        return {'result': 'success'}
    else:
        return {'result': 'failure', 'reason': 'Could not add new item'}


@route('/add/example/:example/<keys:path>')
def add_example_with_items(example, keys):
    """Add multiple items and corresponding example"""
    if Peon(db).addExampleWithItems(example, keys.split('/')):
        return {'result': 'success'}
    else:
        return {'result': 'failure', 'reason': 'Could not add new items'}


@route('/batch/<items:path>')
def batch_add(items):
    """Add multiple items at once"""
    peon = Peon(db)
    results = {}
    for key in items.split('/'):
        if key:
            if peon.addItem(key):
                results[key] = {'result': 'success'}
            else:
                results[key] = {'result': 'failure', 'reason': 'Already in DB'}
    return results


@route('/get/:key')
def get_item(key):
    """ Get existing item """
    return {
        'found': [item.value for item in
                  Key.objects(value=unicode(key, 'utf-8'))]
    }


###############################################################################
# Ajax requests
###############################################################################


import src.app.ajax


###############################################################################
# Utility routes
###############################################################################


@get('/debug')
def debug():
    """Debug info"""
    response.content_type = 'text/plain; charset=utf-8'
    ret = 'Hello world, I\'m %s!\n\n' % os.getpid()
    ret += 'Request vars:\n'
    for k, v in request.environ.iteritems():
        if 'bottle.' in k:
            continue
        ret += '%s=%s\n' % (k, v)

    ret += '\n'
    ret += 'Environment vars:\n'

    for k, v in os.environ.iteritems():
        if 'bottle.' in k:
            continue
        ret += '%s=%s\n' % (k, v)

    return ret


@get('/test')
def test():
    s = request.environ.get('beaker.session')
    s['test'] = s.get('test', 0) + 1
    s.save()
    return 'Test counter: %d' % s['test']


###############################################################################
# Special pages and routes
###############################################################################


@route('/media/<filepath:path>')
def server_static(filepath):
    """Serve static assets"""
    # Note the relative paths!
    return static_file(filepath, root='./media/')


@error(404)
def error404(error):
    """Display insightful message"""
    return render(
        'error',
        message=request.path[1:] + '?! This is not the page you seek, knave!'
    )
