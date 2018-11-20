#!/usr/bin/env bash

# Run phonebook backend tests.

cd $(dirname $0)/import

venv/bin/pytest --flake8

