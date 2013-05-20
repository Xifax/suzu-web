#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    API routes
"""

# Framework
from bottle import route

# Application modules
from src.db.models import Key
from src.db.mongo import connectMongo
from src.run.peon import Peon

# Initialize MongoDB
db = connectMongo()


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
