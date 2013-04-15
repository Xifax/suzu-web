# Suzu

Python web application skeleton (for now).

## General info

Development tools:

* make
* python
* pip
* virtualenv
* node.js
* npm

Uses:

* Python 2.7
* Bottle (python microframework + server)
* Werkzeug (debug tool)
* Jinja2 (templating engine)
* Coffe Script (JS superset)
* Stylus (CSS superset)
* Knockout (MVVM pattern for JS)

Modules and their versions listed in:

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
    - Install virtualenv (using pip or easyinstall)
    - `virtualenv venv --distribute`
    - `source venv/bin/activate`
2. Install `npm`.
3. Run `make init`, it should install required python and npm modules.

## Additional notes

Should probably remove major part of npm_requirements, as it's somewhat not in
use (all compilation is currently happens on client side).

## TODOism

* Implement button 'lookup usages' in right top corner;
* Fix `Weblio` bug, when english examples are shown instead of japanese;
* Another possible button: 'lookup additional usages in Jisho';
* Refactor `routes.py` by separating AJAX, utility and main routes;
* Update radicals compilation;
* Implement filtering and CRUD for `list` route;
* Use jpNetKit instead of code duplication;
* 'Post-process' method for `peon`, should update status (language, pos, etc)
for already added items (when no processing happens [except for unique check],
when adding new items)
