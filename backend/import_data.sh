#!/usr/bin/env bash

PYTHON=$(dirname $0)/venv/bin/python
PROGRAM=$(dirname $0)/import/do_import.py
VAR_DIR=$(dirname $0)/var

source $(dirname $0)/config.sh

# Remove old exported files, if any
rm -rf $VAR_DIR/ous/*
rm -rf $VAR_DIR/employees/*

# Do the deed
API_TOKEN=$API_TOKEN MO_URL=$MO_URL MO_ORG_ROOT=$MO_ORG_ROOT $PYTHON $PROGRAM

# Bail out if there's an error
status=$?

if [ $status -ne 0 ]
then
    echo "Import from MO failed."
    exit 1
fi

# Now transfer to SOLR


# First, clean index for existing data.
$SOLR_POST -c departments -d "<delete><query>*:*</query></delete>"
$SOLR_POST -c employees -d "<delete><query>*:*</query></delete>"

# Reindex
$SOLR_POST -c departments $VAR_DIR/ous
$SOLR_POST -c employees $VAR_DIR/employees

# Clean up after yourself.
rm -rf $VAR_DIR/ous/*
rm -rf $VAR_DIR/employees/*
