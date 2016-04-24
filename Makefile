# Makefile for KISS Python Module.
#
# Source:: https://github.com/ampledata/kiss
# Author:: Greg Albrecht W2GMD <gba@orionlabs.io>
# Copyright:: Copyright 2016 Orion Labs, Inc. and Contributors
# License:: Apache License, Version 2.0
#


.DEFAULT_GOAL := all


all: install_requirements develop

develop:
	python setup.py develop

install:
	python setup.py install

uninstall:
	pip uninstall -y kiss

install_requirements:
	pip install -r requirements.txt

lint:
	pylint -f colorized -r n kiss/*.py tests/*.py *.py || exit 0

flake8:
	flake8 --exit-zero  --max-complexity 12 kiss/*.py tests/*.py *.py

pep8: flake8

clonedigger:
	clonedigger --cpd-output .

publish:
	python setup.py register sdist upload

nosetests:
	python setup.py nosetests

test: lint pep8 nosetests

clean:
	@rm -rf *.egg* build dist *.pyc *.pyo cover doctest_pypi.cfg \
	nosetests.xml pylint.log output.xml flake8.log */*.pyc */*.pyo
