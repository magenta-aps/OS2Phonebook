Documentation for front end developers - how to use the API
===========================================================


Mapping of backend requests (SOLR queries) to application screens
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This document describes how to get the data necessary for displaying the
various pages in the phone book mockup. The document will refer to the
mockups for the web version, but the instructions given are general and
should be understood even without referring to the specific mockups.

If necessary, they can be found in the source code's ``backend/docs/``
directory, in the file ``OS2-telefonbog_webversion.pdf``.

This document follows the mockups, documenting the API by describing the
necessary queries page by page. 

In these examples, the backend (an SOLR server) is assumed to be running
on localhost (``127.0.0.1``) and port 8983. In production, this will be
different, and the URLs should be adjusted accordingly.

.. note::
    For more advanced search combinations than described in this document, see this quick tutorial:

    http://www.solrtutorial.com/solr-query-syntax.html

For more information, please consult the SOLR reference manual:

    http://lucene.apache.org/solr/guide/7_5/overview-of-searching-in-solr.html#overview-of-searching-in-solr

It is possible to combine query parameters in many ways not described
above.

Here, only the SOLR search syntax specifically needed to reproduce the
searches in the mockups is given. Suffice it to say that the full
SOLR/Lucene search syntax has many more features than covered here.

Front page
++++++++++

Root organisation
-----------------

To get the name of the root organisation ("Ballerup Kommune" in the
example), you have two options.

If there is more than one root unit, e.g. because there is more than one
organisation, you need to know the UUID of the root organisation unit.
In the data currently available at ``morademo.magenta-aps.dk``, and
which will be used as an example in this document, this UUID is
``97337de5-6096-41f9-921e-5bed7a140d85``.

In that case, you can get the root node by issuing the following query::
    
    http://127.0.0.1:8983/solr/departments/select?q=uuid:97337de5-6096-41f9-921e-5bed7a140d85

If, on the other hand, you know that there is only one root organisation
unit, you can search for the single root node, denoted by having its
"parent" field set to the value "ROOT"::

   http://127.0.0.1:8983/solr/departments/select?q=parent:ROOT


Note on the data formats in the SOLR results
--------------------------------------------

Org units (departments)
.......................

SOLR will return data in JSON format and according to the following template:

.. sourcecode:: json

    {
        "responseHeader": {
            "status": 0,
            "QTime": 30,
            "params": {
                "q": "*:*",
                "_": "1543400551984"
            }
        },
        "response": {
            "numFound": 1,
            "start": 0,
            "docs": [
                {
                    "document": "<very long string omitted>",
                    "id": "8284b4b5-118a-4cbf-aa7c-f08ae2ca391c",
                    "_version_": 1617934905120915456
                }
            ]
        }
    }

The ``responseHeader`` field contains information about query and query
times and will not concern us here. We will focus on the ``response``
field, which is a list of "``docs``", which are objects found by the
query.

In each of these objects, the fields ``id`` and ``_version_`` are not
used. The actual contents of the found object are in the ``document``
field, which is a JSON encoded string. 

If the ``document`` field of any of these results is parsed, we may,
e.g., get an organisation unit that looks like this:

.. sourcecode:: json

    {
        "associated": [
            [
                "Amin Laurvig Deichgraeber",
                "03ecfcfd-33ab-4d9a-bc46-df4fb9e60ceb",
                "Medhj\u00e6lper",
                "Teknisk Servicemedarb."
            ]
        ],
        "departments": [],
        "employees": [
            [
                "Kadiatou Schultz Petersen",
                "fa42289b-745c-46df-9289-a9f4c155ef19",
                "Ansat",
                "P\u00e6dagoisk vejleder"
            ],
            [
                "Margrethe Neess Borup",
                "5a18ce2b-267a-475d-a781-7f6b714b4e46",
                "Ansat",
                "Teknisk Servicemedarb."
            ]
        ],
        "locations": [
            [
                "DAR",
                "Vesterklit 9, L\u00f8nstrup, 9800 Hj\u00f8rring"
            ]
        ],
        "managers": [
            [
                "Direkt\u00f8r",
                "Margrethe Neess Borup",
                "5a18ce2b-267a-475d-a781-7f6b714b4e46"
            ]
        ],
        "name": "Budget og Planl\u00e6gning",
        "parent": "40644200-b3f1-42d4-8752-8dab581d5b23",
        "uuid": "d4f9af18-aacd-48de-aa78-5f29cb23d716"
    }

Of course, there will be the number of ``docs`` corresponding to the
``numFound`` parameter in the ``response``.

In the present example, there is only one document and the name to be
dislayed is "Budget og Planlægning".  The members are, apart from the
obvious ones, to be interpreted like this:

* ``locations`` are addresses and can be of type ``DAR``, ``EMAIL``
  and ``PHONE``. The list contains a list of addresses; each address is
  itself a pair,  *[type, value]*. As shown in the examples, the
  ``type`` indicates whether this is a postal address, an email address
  or a phone number (e.g., ``"DAR"``) while the ``value`` is a textual representation of
  the address in question (e.g., ``"Skt. Johannes Allé 2, 8000 Aarhus
  C"``).
* ``employees`` correspond to ``engagement`` in MO. They are four-tuples,
  *[name, UUID, engagement type, job function]*.
* ``departments`` are the children of the current node, i.e. the
  subsections etc. They are couples, *[name, UUID]*.
* ``associated`` correspond to ``association`` in MO. They are
  four-tuples, *[name, UUID, association type, job function]*.
* ``managers`` correspond to ``manager`` in MO and are triplets,
  *[manager type, name, UUID]*.


.. note::
    The UUIs for employees, associated and managers are the person
    UUIDs, found under the MO API's ``/e/`` section.

Employees
.........

The result headers are as in the example above - only the contents of
the ``document`` field are different. A typical ``document`` for a
person could be:

.. sourcecode:: json

    {
        "uuid": [
            "cee8800a-983d-41fa-998c-b4557d68ec35"
        ],
        "name": [
            "Anna Bjerre Reidl"
        ],
        "locations": [
            [
                "PHONE",
                "21557342"
            ],
            [
                "DAR",
                "Strandg\u00e5rdsvej 16, Skallerup Klit, 9800 Hj\u00f8rring"
            ],
            [
                "EMAIL",
                "annar@hjorring.dk"
            ]
        ],
        "departments": [
            [
                "IT-Support",
                "d3a9e589-5be0-4d28-95af-5d24ac42a2e9",
                "Ansat",
                "Specialist"
            ]
        ],
        "managing": [
            [
                "Direkt\u00f8r",
                "IT-Support",
                "d3a9e589-5be0-4d28-95af-5d24ac42a2e9"
            ]
        ],
        "id": "e6207b7c-6204-44e2-8839-277694589883",
        "_version_": 1616933478548373504
    }

This record has the following non-trivial (composite) members:

* ``locations`` - this works as for departments.
* ``departments`` - corresponds to ``engagement`` in MO. These are
  four-tuples consisting of *[department name,
  UUID, engagement type, job function]*. Departments in which the person
  is *employed*.
* ``associated`` - corresponds to ``association`` in MO and organized as
  ``departments``. Departments to which the person is associated.
  Association type might e.g. be "Konsulent".
  (tilknyttet).
* ``managing`` - the departments which the user is managing. These are
  triplets consisting of *[department name, UUID, manager type]*.
  Manager type might e.g. be "Afdelingsleder" or "Direktør".


Subdepartments/sections
-----------------------

The names and UUIDs of the departments/sections immediately under the
root may be found in the root doc's ``department`` member, as described
above. 
    
You can access the full data (including phone numbers, etc.) for each of
these subdepartments by doing a query for the corresponding UUID, as we
did with the root department.


Display results (general query)
+++++++++++++++++++++++++++++++

Two separate URLs allow searching for departments or employees::

    http://127.0.0.1:8983/solr/employees/

    http://127.0.0.1:8983/solr/departments/

To search all *employees* - that is, persons - for the name "Eva" in all
supported fields, write::

    http://127.0.0.1:8983/solr/employees/select?q=name:Eva%20locations:Eva%20departments:Eva%20associated:Eva%20managing:Eva

This is an explicit search for the string in all of the fields that are
supported for employees.

In order to search for *departments* in all fields, we do the
corresponding search on the departments URL. 

Since all employees are indexed under the employees URL as given above,
we only need to search for the fields that are *not* directly associated
with any person - which is name and locations.  Supposing that we want
to find all departments that are located on "Havagervej 20, Lønstrup",
we use this URL::

    http://127.0.0.1:8983/solr/departments/select?q=locations:%22Havagervej%2020,%20L%C3%B8nstrup%22

Note that, as in the preceding example, quotes and spaces are URL
encoded. The only important part of this seemingly obscure string is::

    locations:"Havagervej 20, Lønstrup"

Strings match up to the first space, e.g. a search for ``name:Eva Hansen``
in the employees URL will match all persons whose first name is "Eva".
If you wish to match a string exactly, e.g. a name, quotes must be used::

    name:"Eva Hansen"


On the other hand, if you wish to match a prefix that is not terminated
by a space (a very common use case with telefone numbers), use an
asterisk as a wild card - to find all employees whose phone number
starts with 2303, search for ::

    locations:2303*

or, URL-encoded::

    http://127.0.0.1:8983/solr/employees/select?q=locations:2303*


Display results (email search)
++++++++++++++++++++++++++++++

Search for ``locations:<address>`` for full address with an asterisk as
a wildcard of desired, e.g. to get the results for the search in the
mockup, query ::

    http://127.0.0.1:8983/solr/employees/select?q=locations:digi*

for employees/persons and ::

    http://127.0.0.1:8983/solr/departments/select?q=locations:digi*

for departments.

Display results (person search)
+++++++++++++++++++++++++++++++

If there are no spaces in search string, query for ::

    name:<search string>*


Display details (departments)
+++++++++++++++++++++++++++++

Get the unique JSON entry for the department with the desired UUID, ::

    http://127.0.0.1:8983/solr/departments/select?q=uuid:3d3a73c3-7897-4bfb-bed4-fac6d6e19519


Display details (employees)
+++++++++++++++++++++++++++

As for departments, get the selected UUID from the link/search
results/wherever and query for ::

    uuid:<uuid>
