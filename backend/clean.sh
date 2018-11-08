#/usr/bin/env bash

cd $(dirname $0)

# First, stop SOLR to avoid dangling processes.
solr-7.5.0/bin/solr stop

# Remove everything that's not source.
rm -rf solr-7.5.0/ var/ import/__pycache__/ import/venv/
