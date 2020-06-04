Om OS2PhoneBook
===============

Dette er en simpel telefonbog, der henter sine data fra OS2MOs API.

Usage
-----
Start applicationen op med:

.. code-block:: console

    $ docker-compose up --build

Tilføj data til mox databasen:

.. code-block:: console

    $ cat dummy.sql | PGPASSWORD=mox psql -h localhost -U mox

*Note: This data-dump can be acquired from the mo team.*

Start data-import:

.. code-block:: console

    $ docker exec -it os2phonebook_os2phonebook-service_1 python3 cli.py start-import

Dette skridt kan tage flere minutter, og outputtet / fremdriften kan ses med:

.. code-block:: console

    $ docker exec -it os2phonebook_os2phonebook-service_1 tail -f /log/import.log

Licens og Copyright
-------------------

Copyright (c) 2018, Magenta ApS.

Dette værk er frigivet under `Mozilla Public License, version 2.0
<https://www.mozilla.org/en-US/MPL/>`_, som gengivet i ``LICENSE``. 

Dette er et OS2-projekt. Ophavsretten tilhører de individuelle bidragydere.

