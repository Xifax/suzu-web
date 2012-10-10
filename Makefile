update:
	pip install -r requirements.txt --use-mirrors
	npm install

init: update
	make link
	make test

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

launch:
	python suzu.py 8000 &
	sleep 1
	firefox http://localhost:8000 &

kill:
	ps aux | grep 'python suzu.py 8000' | head -1 | cut -d " " -f 3 | xargs kill

compile:
	bin/stylus -u nib -o media/css/ -c media/styl/
	bin/coffee -o media/js/ -c media/coffee/

watch:
	bin/stylus -u nib -o media/css/ -w media/styl/
	bin/coffee -o media/js/ -w media/coffee/

minify:
	echo 'not implemented yet'

link:
	ln -s ./node_modules/.bin ./bin
