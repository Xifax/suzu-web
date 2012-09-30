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

---

## Setting up development environment

1. Initialize virtual environment 'venv'
1.1. Install virtualenv (using pip or easyinstall)
1.2. virtualenv venv --distribute
1.3. source venv/bin/activate
2. Install python modules
3. Install Node.js (preferably, in local environment) and it's modules
3.1. cd bin/
3.2. git clone https://github.com/joyent/node.git
3.3. cd node
3.4. git checkout vLATEST.VERSION
3.5. ./configure --prefix=/path/to/repo/bin/nodejs
3.6. make -j CPU_CORES_NUMBER
3.7. make install
3.8. cd ..
3.9. ln -s nodejs/bin/node node
3.10. ln -s nodejs/bin/npm npm
3.11. INSTALLING MODULES
3.12. ln -s node_modules/coffe-script/bin/coffee coffee
3.13. AAARRGGGHHHHHH

...should really automate this, yep...

<!--Uses virtual environment-->
<!--Uses custom build package-->
<!--All utils are symlinked in bin/-->

## Additional notes

Nothing at the moment.

## TODO:

Implement JS|CSS compiling on launch using Shovel.
