PYTHON=$(dirname $0)/import/venv/bin/python
PROGRAM=$(dirname $0)/import/do_import.py
VAR_DIR=$(dirname $0)/var

MO_URL=http://morademo.atlas.magenta.dk/service
MO_ORG_ROOT=293089ba-a1d7-4fff-a9d0-79bd8bab4e5b

# Remove old exported files, if any
rm -rf $VAR_DIR/*
MO_URL=$MO_URL MO_ORG_ROOT=$MO_ORG_ROOT $PYTHON $PROGRAM
