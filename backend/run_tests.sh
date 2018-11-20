#!/usr/bin/env bash

# Run phonebook backend tests.

python3 -m venv venv
source venv bin/activate
pip install -r import/requirements-test.xml

pushd import
venv/bin/pytest --flake8
popd

rm -rf venv


