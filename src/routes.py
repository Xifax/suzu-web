# Generic libs
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: readme goes here

###############################################################################
# Imports
###############################################################################

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
    jinja2_template as render
)

# Application modules
from src.models import Key
from src.mongo import MongoOnHeroku
#from src.mongo import Mongo
from src.language import Language
from src.weblio import Weblio
from src.mecab import MeCab
from src.peon import Peon

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
try:
    #db = Mongo(db='facts')
    #db.connect()
    #db = MongoOnHeroku('facts')
    #db = MongoOnHeroku('app3405448')
    db = MongoOnHeroku()
except Exception:
   # DB error!
    pass

###############################################################################
# Describing route handling
###############################################################################


@get('/')
def index():
    """Main page"""
    return render('home', name='Anonymous')


@route('/media/<filepath:path>')
def server_static(filepath):
    """Serve static assets"""
    # Note the relative paths!
    return static_file(filepath, root='./media/')


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
                #'reading': reading,
                'readings': readings,
                'translation': translation
            })

        # TODO: add another (optional) key to rout -> response type, json|html
        #return {'term': key, 'data': results}

        return render('lookup', term=key, examples=results)

    else:
        return {'result': 'error', 'reason': 'Unsupported language'}


@route('/add/:key')
def add_item(key):
    """ Add new item """
    if Peon(db).addItem(key):
        return {'result': 'success'}
    else:
        return {'result': 'failure', 'reason': 'Item is already in DB'}


@route('/get/:key')
def get_item(key):
    """ Get existing item """
    return {'found': Key.objects(value=unicode(key, 'utf-8'))}


@route('/list/')
def list_items():
    """ List all items """
    return {'items': [item.value for item in Key.objects]}


@route('/hello/:name')
def say_hello(name):
    """Testing page"""
    greet = {'en': 'Hello'}
    language = req.accept_languages.best_match(greet.keys())
    if language:
        return wz.Response('%s %s!' % (greet[language], name))
    else:
        raise wz.exceptions.NotAcceptable()


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

#@error(404)
#def error404(error):
    #return 'Ooops'
