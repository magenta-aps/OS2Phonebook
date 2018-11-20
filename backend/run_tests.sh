#!/usr/bin/env bash

# Run phonebook backend tests.

DIR=$(dirname $0)
cd $DIR
DIR=$PWD

python3 -m venv $DIR/venv
source $DIR/venv/bin/activate
pip install -r $DIR/import/requirements-test.txt

pushd $DIR/import
$DIR/venv/bin/pytest --flake8
popd

rm -r $DIR/venv


