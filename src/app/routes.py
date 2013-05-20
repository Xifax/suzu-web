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

###############################################################################
# Separate screens
###############################################################################

import src.app.screens

###############################################################################
# Api calls
###############################################################################

import src.app.api

###############################################################################
# Ajax requests
###############################################################################

import src.app.ajax

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


###############################################################################
# Utility routes
###############################################################################


@get('/status')
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
    """Test some random functionality"""
    s = request.environ.get('beaker.session')
    s['test'] = s.get('test', 0) + 1
    s.save()
    return 'Test counter: %d' % s['test']
