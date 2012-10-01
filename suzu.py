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
db = MongoOnHeroku('app3405448')


@route('/add/:key')
def add_item(key):
    ''' Add new item '''
    # TODO: Detect item language
    item = Key(value=key)
    item.save()
    #return item
    return {'status': 'testing'}  # auto-JSON'ed


@route('/get/:key')
def get_item(key):
    ''' Get existing item '''
    #return Key.objects(value=key)
    return {'value': 'testing'}


@route('/hello/:name')
def say_hello(name):
    '''Testing page'''
    greet = {'en': 'Hello'}
    language = req.accept_languages.best_match(greet.keys())
    if language:
        return wz.Response('%s %s!' % (greet[language], name))
    else:
        raise wz.exceptions.NotAcceptable()


@get('/debug')
def debug():
    '''Debug info'''
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
    '''Main page'''
    return render('home', name='Anonymous')


#@error(404)
#def error404(error):
    #return 'Ooops'

# Run application on port provided from cmd (heroku)
bottle.run(host='0.0.0.0', port=sys.argv[1])
