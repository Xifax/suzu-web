init:
	pip install -r requirements.txt --use-mirrors

test:
	nosetests tests

run:
	python suzu.py 8000
