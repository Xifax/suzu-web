# Generic libs
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Implements custom bottle application with different middleware(s)
"""

from beaker.middleware import SessionMiddleware

class StripPath(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, e, h):
        e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
        return self.app(e, h)


class Session(StripPath):

    def __init__(self, app):
        self.app = SessionMiddleware(app, {
            'session.type': 'file',
            'session.data_dir': './session/',
            'session.auto': True,
        })


class CustomApp(Session):

    def __init__(self, app):
        super(CustomApp, self).__init__(app)
