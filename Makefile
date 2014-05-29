# Makefile for KISS Python Module.
#
# Source:: https://github.com/ampledata/kiss
# Author:: Greg Albrecht W2GMD <gba@onbeep.com>
# Copyright:: Copyright 2013 OnBeep, Inc. and Contributors
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

lint: install_requirements
	pylint --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" \
		-r n kiss/*.py tests/*.py || exit 0

pep8: install_requirements
	flake8 --max-complexity 12 --exit-zero kiss/*.py tests/*.py

publish:
	python setup.py register sdist upload

nosetests:
	python setup.py nosetests

test: lint pep8 nosetests

clean:
	@rm -rf *.egg* build dist *.pyc *.pyo cover doctest_pypi.cfg
	nosetests.xml pylint.log output.xml flake8.log */*.pyc */*.pyo
