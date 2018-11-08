#/usr/bin/env bash

POST=solr-7.5.0/bin/post
VAR_DIR=$(dirname $0)/var

# First, clean index for existing data.
$POST -c departments -d "<delete><query>*:*</query></delete>"
$POST -c employees -d "<delete><query>*:*</query></delete>"

# Reindex
$POST -c departments $VAR_DIR/ous
$POST -c employees $VAR_DIR/employees
