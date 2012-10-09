# Generic libs
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Implements custom bottle application with different middleware(s)
"""

#from flup.middleware.gzip import GzipMiddleware


class StripPathMiddleware(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, e, h):
        e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
        return self.app(e, h)


class CustomApp(StripPathMiddleware):

    def __init__(self, app):
        super(CustomApp, self).__init__(app)
        #self.app = GzipMiddleware(app)
