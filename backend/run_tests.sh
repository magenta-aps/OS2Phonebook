#!/usr/bin/env bash

# Run phonebook backend tests.

DIR=$(dirname $0)
cd $DIR
DIR=$PWD

python3 -m venv $DIR/test-venv
source $DIR/test-venv/bin/activate
pip install -r $DIR/import/requirements-test.txt

$DIR/test-venv/bin/pytest --flake8 --junitxml=build/reports/import.xml --cov=import --cov-report=xml --cov-branch  import

rm -r $DIR/test-venv


