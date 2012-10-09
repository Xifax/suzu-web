update:
	pip install -r requirements.txt --use-mirrors
	npm install

init: update
	make link

test:
	nosetests tests

test-unit:
	nosetests tests/unit

test-fun:
	nosetests tests/functional

test-cover:
	nosetests --cover-html-dir=docs

run:
	python suzu.py 8000

compile:
	bin/stylus -o media/css/ -c media/styl/
	bin/coffee -o media/js/ -c media/coffee/

watch:
	bin/stylus -o media/css/ -w media/styl/
	bin/coffee -o media/js/ -w media/coffee/

link:
	ln -s ./node_modules/.bin ./bin
