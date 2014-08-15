#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    AJAX requests routes
"""

# Stdlib
from json import dumps, loads
import random
from datetime import timedelta, date

# Framework
from bottle import (
    route,
    request,
    response
)

# Application modules
from src.db.models import Key
from src.db.mongo import connectMongo
from src.db.storage import Storage

from src.api.jp.weblio import Weblio
from src.api.jp.wordnet import Wordnet
from src.api.jp.jisho import Jisho

from src.run.peon import Peon


# Initialize MongoDB
db = connectMongo()
# Initialize Redis
store = Storage()


@route('/examples/:term')
def get_examples(term):
    """Lookup examples for item in Weblio"""
    term = unicode(term, 'utf-8')
    examples = Weblio().examples(term)
    return {'examples': examples}


@route('/similar/:term')
def get_similar(term):
    """Lookup similar words for item in Weblio"""
    term = unicode(term, 'utf-8')
    similar = [item['translate'] for item in Wordnet().lookup(term)]
    # TODO: remove identical words
    return {'similar': similar}


@route('/info/:term')
def get_info(term):
    """Lookup info for left and right toolbars simultaneously"""
    term = unicode(term, 'utf-8')
    return {
        'details': Jisho().details(term),
        'examples': Weblio().examples(term)
    }


@route('/kanji_info/:kanji')
def get_kanji_info(kanji):
    """Lookup info for single kanji"""
    kanji = unicode(kanji, 'utf-8')
    return {'info': Jisho().details(kanji)}


@route('/related/:radical')
def related_kanji(radical):
    """List all related kanji for specified radical (AJAX) """
    response.content_type = 'application/json'
    radical = unicode(radical, 'utf-8')
    # Display 10-20 randomized kanji
    # TODO: make random sampling optional?
    try:
        return dumps(random.sample(
            set(store.find_kanji_with_radical(radical)), 30)
        )
    except ValueError:
        return dumps(store.find_kanji_with_radical(radical))


@route('/toggle')
def toggle():
    """Toggle toolbar status on page load"""
    session = request.environ.get('beaker.session')
    session['toggled'] = not session.get('toggled', False)
    session.save()
    return {'status': session['toggled']}


@route('/toggled')
def toggled():
    """Check toolbar status status"""
    session = request.environ.get('beaker.session')
    return {'status': session.get('toggled', False)}


@route('/list_all')
def list_all():
    """ List all (AJAX) """
    items = []
    for i, item in enumerate(Key.objects()):
        items.append({
            'id': i,
            'value': item.value,
            'added': item.added.strftime("%Y-%m-%d %H:%M:%S"),
            'pos': item.pos,
            'status': item.status,
            'category': item.category,
            'lang': item.lang,
        })

    # NB: bottle allows only dictionary serialization
    response.content_type = 'application/json'
    return dumps(items)


@route('/lock')
def lock():
    """Lock|unlock kanji for today"""
    if request.get_cookie('lock'):
        response.delete_cookie('lock')
        return {'result': 'unlocked'}
    else:
        # Set kanji for today
        kanji_id = str(Peon(db).random().id)
        next_day = date.today() + timedelta(days=1)
        response.set_cookie(
            'lock',
            kanji_id,
            secret='secret',
            expires=next_day,
            path='/'
        )
        return {'result': 'locked', 'id': kanji_id}


@route('/toggle_favorite/:kanji')
def toggle_favorite(kanji):
    """Toggle kanji as favorite"""
    kanji = unicode(kanji, 'utf-8')
    favorites = request.get_cookie('favorites', secret='secret')

    # Check if cookie exists
    if favorites:
        # Load json and add/remove kanji from favorites
        favorites = loads(favorites)
        if kanji in favorites:
            favorites.remove(kanji)
            result = 'unfav'
        else:
            favorites.append(kanji)
            result = 'fav'
    # Otherwise, initialize cookie
    else:
        favorites = [kanji]
        result = 'fav'

    in_far_future = date.today() + timedelta(days=360)
    response.set_cookie(
        'favorites',
        # Serialize kanji list
        dumps(favorites),
        secret='secret',
        path='/',
        expires=in_far_future
    )
    return {'result': result}
