# Suzu

Python web application skeleton (for now).

## General info

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

## Project structure

    bin/    -> executables
    lib/    -> NodeJS and Python modules
    media/  -> static assets (css, images, etc)
    views/  -> templates
    src/    -> project modules

## Setting up development environment

1. Initialize virtual environment 'venv'
    - Install virtualenv (using pip or easyinstall)
    - virtualenv venv --distribute
    - source venv/bin/activate
2. Install python modules
3. Install Node.js (preferably, in local environment) and it's modules
    - bin/
    - git clone https://github.com/joyent/node.git
    - cd node
    - git checkout vLATEST.VERSION
    - ./configure --prefix=/path/to/repo/bin/nodejs
    - make -j CPU_CORES_NUMBER
    - make install
    - cd ..
    - ln -s nodejs/bin/node node
    - ln -s nodejs/bin/npm npm
    - INSTALLING MODULES
    - ln -s node_modules/coffe-script/bin/coffee coffee
    - AAARRGGGHHHHHH

...should really automate this, yep...

## Additional notes

Nothing at the moment.

## TODO:

Implement JS|CSS compiling on launch using Shovel|make
