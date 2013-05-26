all: init test

init:
	pip install tox coverage

test:
	coverage erase
	tox
	coverage html
