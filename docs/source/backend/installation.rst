
Installation
============

To check out the source code and quickly install the backend, execute
the following on a computer with a modern version of GNU/Linux::

    git clone https://github.com/os2mo/os2phonebook
    cd os2phonebook/backend
    ./install.sh

.. note::

    This requires an Internet connection. It was tested on Ubuntu 18.04
    and 16.04.

    It also requires Java 8 or newer and Python 3.5 or newer. This phone
    book will *not* work with older versions of Java or Python.

.. note::

    These instructions cover how to set up the system for development
    purposes. Please refer to the SOLR documentation for instructions on
    deploying SOLR for production.

To import data to the system, you need to modify the variables
``MO_URL`` and ``MO_ORG_ROOT`` in the ``import_data.sh`` script. After
doing this, simply run the command ::

    ./import_data.sh

This command will run for a while, downloading all employees and
organisation units corresponding to the given ``MO_ORG_ROOT``.

Once it is done, the backend is up and running and ready for the front
end to use. SOLR will be running and listening on ``localhost:8983``.

Uninstall
---------

To uninstall the phonebook backend, go to the backend source directory
as indicated above and run the command::

    ./clean.sh

This will remove the Python dependencies as well as the SOLR instance.




