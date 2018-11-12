Mapping of backend requests (SOLR queries) to application screens
=================================================================

This document describes how to get the data necessary for displaying the
various pages in the phone book mockup. The document will refer to the
mockups for the web version. These mockups may be found in the same
directory as the present document, in the file
``OS2-telefonbog_webversion.pdf``.

The document follows the mockups, describing the necessary queries page
by page. 

In these examples, the backend (an SOLR server) is assumed to be running
on localhost (``127.0.0.1``) and port 8983. In production, this will be
different, and the URLs should be adjusted accordingly.

Note that only the SOLR search syntax specifically needed to reproduce
the searches in the mockups is given. At the end of the document, a link
is given to a more complete coverage of the SOLR/Lucene search syntax,
which has many more features than covered here.

Front page
==========

Root organisation
-----------------

To get the name of the root organisation ("Ballerup Kommune" in the
example), you have two options.

In the first case, you rely on the assumption that this organisation has
one root organisation unit only. In that case, you can search for the
single root node, denoted by having its "parent" field set to the value
"ROOT": ::

   http://127.0.0.1:8983/solr/departments/select?q=parent:ROOT

If you cannot make that assumption, e.g. because there are more than one
organisation and hence more than one root unit, you need to know the
UUID of the root organisation unit. In the data currently available at
``morademo.magenta-aps.dk``, and which will be used as an example in
this document, this UUID is ``97337de5-6096-41f9-921e-5bed7a140d85``.

In that case, you can get the root node by issuing the following query:
::
    
    http://127.0.0.1:8983/solr/departments/select?q=uuid:97337de5-6096-41f9-921e-5bed7a140d85


Note on the data formats in the SOLR results
--------------------------------------------

Org units (departments)
.......................

SOLR will return data in JSON format and according to the following template: ::

    {
    "responseHeader":{
     (...)
     },
    "response":{"numFound":1,"start":0,"docs":[
      {
        "uuid":["97337de5-6096-41f9-921e-5bed7a140d85"],
        "name":["Hjørring"],
        "parent":["ROOT"],
        "locations":["DAR",
          "Stensgårdsvej 19, Nr Harritsl, 9800 Hjørring"],
        "employees":["Esther Hildeborg Nielsen",
          "2355a754-5de4-4b3f-b78c-0dceba80dfa6",
          "Ergoterapeut",
          (...)
          "Pawel Nyskov Dalgaard",
          "edb1f226-90db-4d23-94d2-232c048f84de",
          "Jurist"],
        "departments":["Borgmesterens Afdeling",
          "40644200-b3f1-42d4-8752-8dab581d5b23",
          (...)
          "Teknik og Miljø",
          "be7bb9e5-b298-4019-b0fd-ce80c8f97934"],
        "associated":[
          "Christian Kjeldal Schmidt Nielsen",
          "4419dbb3-a698-4d98-b255-a4eff621ee4f",
          "Problemknuser",
          "Specialkonsulent"],
        "managers":["Direktør",
          "Esther Hildeborg Nielsen",
          "b078107a-4299-4251-b41c-23e0b8a9575a"],
        "id":"38bbb6ad-d31f-4381-aa88-61be37f70d8c",
        "_version_":1616659562091249664}]
     }}

Of course, there will be the number of ``docs`` corresponding to the
``numFound`` parameter in the ``response``.

In the present example, there is only one document and the name to be
dislayed is simply "Hjørring".  The members are, apart from the obvious
ones, to be interpreted like this:

* ``locations`` are addresses and can be of type ``DAR``, ``EMAIL``
  and ``PHONE``. The list contains a list of addresses that are to be
  interpreted as couples, *(type, value)*.
* ``employees`` correspond to ``engagement`` in MO. They are four-tuples,
  *(name, UUID, engagement type, job function)*.
* ``departments`` are the children of the current node, i.e. the
  subsections etc. They are couples, *(name, UUID)*.
* ``associated`` correspond to ``association`` in MO. They are
  four-tuples, *(name, UUID, association type, job function)*.
* ``managers`` correspond to ``manager`` in MO and are triplets,
  *(manager type, name, UUID)*.


**NOTE:** The UUIs for employees, associated and managers are the person
UUIDs, found under the MO API's ``/e/`` section.

Employees
.........

The "wrapping" with response headers etc. is like for departments. A
typical "doc" for a person could be: ::

    {
        "uuid":["cee8800a-983d-41fa-998c-b4557d68ec35"],
        "name":["Anna Bjerre Reidl"],
        "locations":["PHONE",
          "21557342",
          "DAR",
          "Strandgårdsvej 16, Skallerup Klit, 9800 Hjørring",
          "EMAIL",
          "annar@hjorring.dk"],
        "departments":["IT-Support",
          "d3a9e589-5be0-4d28-95af-5d24ac42a2e9",
          "Ansat",
          "Specialist"],
        "managing":["Direktør",
          "IT-Support",
          "d3a9e589-5be0-4d28-95af-5d24ac42a2e9"],
        "id":"e6207b7c-6204-44e2-8839-277694589883",
        "_version_":1616933478548373504
    }


This record has the following non-trivial members:

* ``locations`` - this works as for departments.
* ``departments`` - corresponds to ``engagement`` in MO. These are
  to be interpreted as four-tuples consisting of *(department name,
  UUID, engagement type, job function)*. Departments in which the person
  is *employed*.
* ``associated`` - corresponds to ``association`` in MO and organized as
  ``departments``. Departments to which the person is associated.
  Association type might e.g. be "Konsulent".
  (tilknyttet).
* ``managing`` - the departments which the user is managing. These are
  triplets consisting of *(department name, UUID, manager type)*.
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
===============================

There are two separate URLs for searching departments, basically ::

    http://127.0.0.1:8983/solr/employees/

    http://127.0.0.1:8983/solr/departments/

To search for *persons* or *employees* in all supported fields, write
(e.g., searching for the name "Eva"): ::

    http://127.0.0.1:8983/solr/employees/select?q=name:Eva%20locations:Eva%20departments:Eva%20associated:Eva%20managing:Eva

I.e., this is an explicit search for the string in all of the fields
that are supported for employees. 

In order to search for *departments* in all fields, we do the
corresponding search on the departments URL. 

Since all employees (persons, Users in LoRa) are indexed under the employees URL
as given above, we only need to search for the fields that are *not*
directly associated with any person - which is name and locations.
Supposing that we want to find all departments that are located on
"Havagervej 20, Lønstrup", we use this URL: ::

    http://127.0.0.1:8983/solr/departments/select?q=locations:%22Havagervej%2020,%20L%C3%B8nstrup%22

Note that, as in the preceding example, quotes and spaces are URL
encoded. The only important part of this seemingly obscure string is: ::

    locations:"Havagervej 20, Lønstrup"

Strings match up to the first space, e.g. a search for ``name:Eva Hansen``
in the employees URL will match all persons whose first name is "Eva".
If you wish to match a string exactly, e.g. a name, quotes must be used: ::

    name:"Eva Hansen"


On the other hand, if you wish to match a prefix that is not terminated
by a space (a very common use case with telefone numbers), use an
asterisk as a wild card - to find all employees whose phone number
starts with 2303, search for ::

    locations:2303*

or, URL-encoded: ::

    http://127.0.0.1:8983/solr/employees/select?q=locations:2303*


Display results (email search)
==============================

Search for ``locations:<address>`` for full address with an asterisk as
a wildcard of desired, e.g. to get the results for the search in the
mockup, query ::

    http://127.0.0.1:8983/solr/employees/select?q=locations:digi*

for employees/persons and ::

    http://127.0.0.1:8983/solr/departments/select?q=locations:digi*

for departments.

Display results (person search)
===============================

If there are no spaces in search string, query for ::

    name:<search string>*

**Note:** For more advanced search combinations than described here,
please refer to this section of the SOLR Tutorial,

    http://www.solrtutorial.com/solr-query-syntax.html

It is possible to combine query parameters in many ways not described
above.


Display details (departments)
=============================

Get the unique JSON entry for the department with the desired UUID, ::

    http://127.0.0.1:8983/solr/departments/select?q=uuid:3d3a73c3-7897-4bfb-bed4-fac6d6e19519


Display details (employees)
===========================

As for departments, get the selected UUID from the link/search
results/wherever and query for ::

    uuid:<uuid>

