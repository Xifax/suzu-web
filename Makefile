init:
	pip install -r requirements.txt --use-mirrors
	npm install

#env:
	#$(source venv/bin/activate)

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
	node_modules/stylus/bin/stylus media/css

watch:
	node_modules/stylus/bin/stylus -w media/css

