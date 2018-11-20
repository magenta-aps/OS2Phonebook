#!/usr/bin/env bash

# Run phonebook backend tests.

cd $(dirname $0)

python3 -m venv venv
source venv/bin/activate
pip install -r $PWD/import/requirements-test.txt

pushd import
venv/bin/pytest --flake8
popd

rm -rf venv


