#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: readme goes here

# Generic libs
import os
import sys

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
from src.mongo import MongoOnHeroku
from src.models import Key

# Initialize Werkzeug plugin
wz = bottle_werkzeug.Plugin(evalex=True)  # should work without True
bottle.install(wz)
# Enable debug mode
bottle.debug(True)
# Process request by Werkzeug
req = wz.request
# Update paths
#TEMPLATE_PATH.append('./views')

#from mongoengine import connect
#connect('facts')

# Initialize MongoDB
#db = Mongo(db='facts', host='127.0.0.1', port=27818)
#db = Mongo(db='facts')
#db.connect()
#db = MongoOnHeroku('facts')
#db = MongoOnHeroku('app3405448')

@route('/lookup/:key')
def lookup_item(key):
    """Looks up item definition, translations, readings, examples and so on"""
    # Convert key to unicode
    key = unicode(key, 'utf-8')
    # TODO: profile & move to controller|processor, etc
    from src.language import Language
    from src.weblio import Weblio
    from src.mecab import MeCab
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
            reading = mecab.reading(example)
            results.append({
                'example': example,
                'reading': reading,
                'translation': translation
            })

        # TODO: add another (optional) key to rout -> response type, json|html
        #return {'term': key, 'data': results}
        # TODO: add ruby css :
        '''
        ruby > rt, ruby > rbc + rtc {
            font-size: 60%;
            letter-spacing: 0px;
            display: table-header-group;
        }
        OR
        ruby { display: inline-table; text-align: center; white-space: nowrap; text-indent: 0; margin: 0; vertical-align: bottom; }
        ruby > rb, ruby > rbc { display: table-row-group; }
        ruby > rt, ruby > rbc + rtc { display: table-header-group; font-size: 60%; letter-spacing: 0; }
        ruby > rbc + rtc + rtc { display: table-footer-group; font-size: 60%; letter-spacing: 0; }
        rbc > rb, rtc > rt { display: table-cell; letter-spacing: 0; }
        rtc > rt[rbspan] { display: table-caption; }
        rp { display: none; }
        SEE
        http://html5doctor.com/ruby-rt-rp-element/
        http://oli.jp/example/ruby/
        http://po-ru.com/diary/retrofitting-furigana-to-browsers/
        Better still, single jscript:
        https://github.com/threedaymonk/furigana-shim
        '''
        return render('lookup', term=key, examples=results)

    else:
        return {'result': 'error', 'reason': 'Unsupported language'}

@route('/add/:key')
def add_item(key):
    """ Add new item """
    # TODO: Detect item language
    # TODO: check, if such language is available
    # TODO: if not, reject with message
    # TODO: else, add new item and mark as 'unprepared'
    item = Key(value=key)
    item.save()
    #return item
    return {'status': 'testing'}  # auto-JSON'ed


@route('/get/:key')
def get_item(key):
    """ Get existing item """
    #return Key.objects(value=key)
    return {'value': 'testing'}


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


@get('/')
def index():
    """Main page"""
    return render('home', name='Anonymous')


#@route('/media/js/<filename:re:.*\.js>#')
#def send_image(filename):
    #return static_file(filename, root='/media/js/', mimetype='image/png')


@route('/media/<filepath:path>')
def server_static(filepath):
    """Serve static assets"""
    # Note the relative paths!
    return static_file(filepath, root='./media/')


#@error(404)
#def error404(error):
    #return 'Ooops'

# Run application on port provided from cmd (heroku)
bottle.run(host='0.0.0.0', port=sys.argv[1])
