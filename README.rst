Om OS2PhoneBook
===============

Dette er en simpel telefonbog, der henter sine data fra OS2MOs API.

Usage
-----
Start applicationen op med:

.. code-block:: console

    $ docker-compose up --build

Start en OS2MO op, og tilføj data til mox databasen:

.. code-block:: console

    $ cat dev-environment/snapshot/kolding-fixtures.sql | PGPASSWORD=mox psql -h localhost -U mox

Hent os2mo-data-import-and-export, og start et data-import:

.. code-block:: console

    $ ./tools/job-runner.sh exports_os2phonebook_export

Dette skridt kan tage flere minutter, og outputtet / fremdriften kan ses med:

Licens og Copyright
-------------------

Copyright (c) 2018, Magenta ApS.

Dette værk er frigivet under `Mozilla Public License, version 2.0
<https://www.mozilla.org/en-US/MPL/>`_, som gengivet i ``LICENSE``. 

Dette er et OS2-projekt. Ophavsretten tilhører de individuelle bidragydere.

