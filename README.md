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

Nothing at the moment.
