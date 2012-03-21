#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import os

#from flask import Flask
#app = Flask(__name__)

#@app.route('/')
#def hello():
    #return 'Hello World!'

#if __name__ == '__main__':
    ## Bind to PORT if defined, otherwise default to 5000.
    #port = int(os.environ.get('PORT', 5000))
    #app.run(host='0.0.0.0', port=port)
    
#from bottle import route, run

##@route('/hello/:name')
#@route('/')
#def index(name='World'):
    #return '<b>Hello %s!</b>' % name

#run(host='0.0.0.0', port=5000)
##run(host='localhost', port=8080)

import os
from os import environ as env
from sys import argv

import bottle
from bottle import default_app, request, route, response, get

bottle.debug(True)

@get('/')
def index():
    response.content_type = 'text/plain; charset=utf-8'
    ret = 'Hello world, I\'m %s!\n\n' % os.getpid()
    ret += 'Request vars:\n'
    for k, v in request.environ.iteritems():
        if 'bottle.' in k:
            continue
        ret += '%s=%s\n' % (k, v)

    ret += '\n'
    ret += 'Environment vars:\n'

    for k, v in env.iteritems():
        if 'bottle.' in k:
            continue
        ret += '%s=%s\n' % (k, v)

    return ret

bottle.run(host='0.0.0.0', port=argv[1])
