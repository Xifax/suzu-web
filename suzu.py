#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: readme goes here

# Generic libs
import sys

# Framework modules
from bottle import app, run

# Application modules
from src.app.middleware import CustomApp
import src.app.routes


# Run application on port provided from cmd (heroku)
run(app=CustomApp(app()), host='0.0.0.0', port=sys.argv[1])
