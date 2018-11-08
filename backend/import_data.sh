PYTHON=$(dirname $0)/import/venv/bin/python
PROGRAM=$(dirname $0)/import/do_import.py
VAR_DIR=$(dirname $0)/var

MO_URL=http://morademo.atlas.magenta.dk/service
MO_ORG_ROOT=293089ba-a1d7-4fff-a9d0-79bd8bab4e5b

# Remove old exported files, if any
rm -rf $VAR_DIR/ous/*
rm -rf $VAR_DIR/employees/*

# Do the deed
MO_URL=$MO_URL MO_ORG_ROOT=$MO_ORG_ROOT $PYTHON $PROGRAM

# Now transfer to SOLR

SOLR_POST=solr-7.5.0/bin/post

# First, clean index for existing data.
$SOLR_POST -c departments -d "<delete><query>*:*</query></delete>"
$SOLR_POST -c employees -d "<delete><query>*:*</query></delete>"

# Reindex
$SOLR_POST -c departments $VAR_DIR/ous
$SOLR_POST -c employees $VAR_DIR/employees

# Clean up after yourself.
rm -rf $VAR_DIR/ous/*
rm -rf $VAR_DIR/employees/*
