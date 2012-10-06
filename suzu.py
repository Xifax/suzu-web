#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: readme goes here

# Generic libs
import sys

# Framework modules
from bottle import run

# Application modules
import src.routes

# Run application on port provided from cmd (heroku)
run(host='0.0.0.0', port=sys.argv[1])
