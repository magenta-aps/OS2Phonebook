Architecture
============

The os2phonebook backend consists of two components:

* A Python program (located in the ``import`` directory) that imports
  all the necessary data from MO and stores it in the file system, and
* An SOLR server in which the data are indexed, and from which the
  frontend retrieves them.

This corresponds to the two steps in the ``import_data.sh`` script.

The phonebook is supposed to be kept up to date by importing and
reindexing regularly, normally once a day. When reindexing, the SOLR
data are completely removed and reimported, which means that data may be
unavailable for a brief period of time during the updates. This could be
remedied in several ways, e.g. for caching, if it turns out to be a
problem.
