# Suzu

Handy tool for aggregating kanji, compounds and related examples.
Also displays some random kanji from collection on title page, usages,
radical decomposition and examples included.

Application is currently deployed on Heroku: http://suzu.herokuapp.com

## General info

Development tools:

* make
* python
* pip
* virtualenv
* npm
* watchdog

Uses:

* Python 2.7
* Bottle (python microframework)
* Gunicorn (server with workers)
* Werkzeug (debug tool)
* Jinja2 (templating engine)
* Coffe Script (JS superset)
* Stylus (CSS superset)

Required modules and their versions are listed in:

* requirements.txt
* npm_requirements.txt
* package.json

## Project structure

    bin/    -> executables
    lib/    -> NodeJS and Python modules
    media/  -> static assets (css, images, etc)
    views/  -> templates
    src/    -> project modules

## Setting up development environment

1. Initialize virtual environment 'venv':
    - Install virtualenv (using pip or easy_install)
    - `virtualenv venv --distribute`
    - `source venv/bin/activate`
2. Install `npm`;
3. Run `make init`, it should install required python and npm modules;
4. Run `make run` to launch application;
5. Run `make watch` to reload server and/or recompile styles/js on code change.

## Additional notes

Should probably remove major part of npm_requirements, as it's somewhat not in
use (all compilation is currently happens on developer side).

## TODOism

* Fix `Weblio` bug, when english examples are shown instead of japanese;
* Another possible button: 'lookup additional usages in Jisho';
* Refactor `routes.py` by separating AJAX, utility and main routes;
* Use jpNetKit instead of code duplication;
* 'Post-process' method for `peon`, should update status (language, pos, etc)
for already added items (when no processing happens [except for unique check],
when adding new items)
