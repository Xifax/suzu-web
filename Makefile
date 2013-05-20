update:
	pip install -r requirements.txt --use-mirrors
	npm install

init: update
	make link
	make test

test:
	nosetests tests

test-print:
	nosetests tests --nocapture

test-unit:
	nosetests tests/unit

test-fun:
	nosetests tests/functional

test-cover:
	nosetests --cover-html-dir=docs

run: compile
	python suzu.py 8000

launch:
	python suzu.py 8000 &
	sleep 1
	firefox http://localhost:8000 &

kill:
	ps aux | grep 'python suzu.py 8000' | head -1 | cut -d " " -f 3 | xargs kill

compile:
	node_modules/.bin/grunt

watch:
	node_modules/.bin/grunt watch
	watchmedo shell-command \
		--patterns="*.py" \
		--recursive \
		--command='pkill -HUP python'\
		.

link:
	ln -s ./node_modules/.bin ./bin
