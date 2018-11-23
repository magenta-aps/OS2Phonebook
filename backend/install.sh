#/usr/bin/env bash
# NOTE: This installer is for development purposes. It is designed to
# get up and running quickly.
#
# A production deployment may have other requirements.

# Prerequisites

# Only try to install dependencies if we actually need them.

PKG_FILE=/tmp/installed-package-list.txt
DEPENDENCIES="python3-venv default-jre"
TO_INSTALL=""

dpkg -l | grep "^ii" > $PKG_FILE

for PACKAGE in ${DEPENDENCIES}
do
    if ! grep -wq "ii  $PACKAGE " $PKG_FILE
    then
        TO_INSTALL=$TO_INSTALL" "$PACKAGE
    fi
done
if [ "$TO_INSTALL" != "" ]
then
    echo "Installing: " $TO_INSTALL
    if ! sudo apt-get -qq update
    then
        echo "ERROR: Apt repositories are not valid or cannot be reached from your network." 1>&2
        echo "Please fix and retry" 1>&2
        exit -1
    else
        echo "Installing dependencies ..."
        sudo apt-get -qy install $TO_INSTALL
    fi
fi

# Dependencies done, do the installation itself.

# We'll work here
cd $(dirname $0)

if [ ! -d "solr-7.5.0" ]
then

    #Get SOLR
    wget http://dk.mirrors.quenda.co/apache/lucene/solr/7.5.0/solr-7.5.0.tgz

    # Verify SOLR download
    if shasum -s -c docs/solr.sha1 
    then 
        echo 'SOLR download OK'
    else 
        echo 'SOLR download failed!'
        exit 1
    fi

    tar xvf solr-7.5.0.tgz
    rm solr-7.5.0.tgz

    solr-7.5.0/bin/solr start
    solr-7.5.0/bin/solr create -c departments -s 2 -rf 2
    solr-7.5.0/bin/solr create -c employees -s 2 -rf 2

    # Create schema for departments
    
   curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field": {"name":"document", "type":"text_general", "multiValued":false, "stored":true, indexed: false}}' http://localhost:8983/solr/departments/schema
   curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field": {"name":"name", "type":"text_general", "multiValued":false, "stored":false}}' http://localhost:8983/solr/departments/schema
    curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field": {"name":"uuid", "type":"text_general", "multiValued":false, "stored":false}}' http://localhost:8983/solr/departments/schema
    curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field": {"name":"parent", "type":"text_general", "multiValued":false, "stored":false}}' http://localhost:8983/solr/departments/schema
    curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field": {"name":"locations", "type":"text_general", "multiValued":true, "stored":false}}' http://localhost:8983/solr/departments/schema
    curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field": {"name":"employees", "type":"text_general", "multiValued":true, "stored":false}}' http://localhost:8983/solr/departments/schema
    curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field": {"name":"departments", "type":"text_general", "multiValued":true, "stored":false}}' http://localhost:8983/solr/departments/schema
    curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field": {"name":"associated", "type":"text_general", "multiValued":true, "stored":false}}' http://localhost:8983/solr/departments/schema
    curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field": {"name":"managers", "type":"text_general", "multiValued":true, "stored":false}}' http://localhost:8983/solr/departments/schema

  # Create schema for employees
   curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field": {"name":"document", "type":"text_general", "multiValued":false, "stored":true, indexed: false}}' http://localhost:8983/solr/employees/schema
    curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field": {"name":"name", "type":"text_general", "multiValued":false, "stored":false}}' http://localhost:8983/solr/employees/schema
    curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field": {"name":"uuid", "type":"text_general", "multiValued":false, "stored":false}}' http://localhost:8983/solr/employees/schema
    curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field": {"name":"locations", "type":"text_general", "multiValued":true, "stored":false}}' http://localhost:8983/solr/employees/schema
    curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field": {"name":"departments", "type":"text_general", "multiValued":true, "stored":false}}' http://localhost:8983/solr/employees/schema
    curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field": {"name":"associated", "type":"text_general", "multiValued":true, "stored":false}}' http://localhost:8983/solr/employees/schema
    curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field": {"name":"managing", "type":"text_general", "multiValued":true, "stored":false}}' http://localhost:8983/solr/employees/schema

    echo "SOLR installed, SOlR started."


else
    echo "SOLR already installed; use solr-7.5.0/bin/solr status to check."
fi

# Install importer

if [ ! -d "venv" ]
then
    python3 -m venv venv
fi
source venv/bin/activate

pip install -r import/requirements.txt

echo "Everything installed."
echo ""
echo "Run import_data.sh to get started."
