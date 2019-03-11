#/usr/bin/env bash

cd $(dirname $0)

# First, stop SOLR to avoid dangling processes.
if [ -f solr-7.7.1/bin/solr ]
then
    solr-7.7.1/bin/solr stop -all
fi

# Remove everything that's not source.
rm -rf solr-7.7.1/ var/ import/__pycache__/ venv/ build/ coverage.xml
