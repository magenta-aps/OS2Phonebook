#/usr/bin/env bash
# NOTE: This installer is for development purposes. It is designed to
# get up and running quickly.
#
# A production deployment may have other requirements.

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

    echo "SOLR installed, SOlR started."
else
    echo "SOLR already installed; use solr-7.5.0/bin/solr status to check."
fi

# Install importer

cd import
if [ ! -d "venv" ]
then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt

echo "Everything installed."
echo ""
echo "Run import_data.sh and index_solr.sh to get started."



