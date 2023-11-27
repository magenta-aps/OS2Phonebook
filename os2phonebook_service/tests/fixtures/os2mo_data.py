# Fixtures
# These fixtures simulate the content returned by os2mo
from typing import List


def organisation() -> List[dict]:
    """Get organisations from os2mo

    GET /service/o/

    Returns:
        List[dict]: A list of os2mo organisation objects

    """

    return [
        {
            "name": "Kolding Kommune",
            "user_key": "Kolding Kommune",
            "uuid": "3b866d97-0b1f-48e0-8078-686d96f430b3",
        }
    ]


def org_unit() -> dict:
    """Get organisation from os2mo

    GET /service/o/ou/3b866d97-0b1f-48e0-8078-686d96f430b3

    Returns:
        dict: An os2mo organisation object

    """

    return {
        "location": "",
        "name": "Kolding Kommune",
        "org": {
            "name": "Kolding Kommune",
            "user_key": "Kolding Kommune",
            "uuid": "3b866d97-0b1f-48e0-8078-686d96f430b3",
        },
        "org_unit_level": {
            "example": None,
            "name": "N1",
            "scope": "TEXT",
            "user_key": "N1",
            "uuid": "84f95e29-48a0-4175-85fd-84a1f596e1a4",
        },
        "org_unit_type": {
            "example": None,
            "name": "Afdeling",
            "scope": "TEXT",
            "user_key": "Afdeling",
            "uuid": "9d2ac723-d5e5-4e7f-9c7f-b207bd223bc2",
        },
        "parent": None,
        "time_planning": {
            "example": None,
            "name": "Dannes ikke",
            "scope": "TEXT",
            "user_key": "Dannes ikke",
            "uuid": "25b83672-e7aa-4206-9ede-36ef0df4857a",
        },
        "user_key": "Kolding Kommune",
        "user_settings": {
            "orgunit": {
                "show_level": True,
                "show_location": True,
                "show_org_unit_button": False,
                "show_primary_association": True,
                "show_primary_engagement": True,
                "show_roles": True,
                "show_time_planning": True,
                "show_user_key": True,
            }
        },
        "uuid": "f06ee470-9f17-566f-acbe-e938112d46d9",
        "validity": {"from": "1960-01-01", "to": None},
    }


def org_unit_addresses() -> List[dict]:
    """Get organisation address details from os2mo

    GET /service/o/ou/3b866d97-0b1f-48e0-8078-686d96f430b3/details/address

    Returns:
        List[dict]: A list of related address type objects

    """

    return [
        {
            "address_type": {
                "example": None,
                "name": "Email",
                "scope": "EMAIL",
                "user_key": "EmailUnit",
                "uuid": "61c22b75-01b0-4e83-954c-9cf0c8dc79fe",
            },
            "href": "mailto:info@kolding.dk",
            "name": "info@kolding.dk",
            "org_unit": {
                "name": "Kolding Kommune",
                "user_key": "Kolding Kommune",
                "uuid": "f06ee470-9f17-566f-acbe-e938112d46d9",
                "validity": {"from": "1960-01-01", "to": None},
            },
            "user_key": "info@kolding.dk",
            "uuid": "27297ea5-06ea-4e75-bd77-547bd1fad8e7",
            "validity": {"from": "1960-01-01", "to": None},
            "value": "info@kolding.dk",
        },
        {
            "address_type": {
                "example": None,
                "name": "Webadresse",
                "scope": "WWW",
                "user_key": "WebUnit",
                "uuid": "575b6d01-61a1-4d5f-8b55-b432d25fd826",
            },
            "href": None,
            "name": "www.kolding.dk",
            "org_unit": {
                "name": "Kolding Kommune",
                "user_key": "Kolding Kommune",
                "uuid": "f06ee470-9f17-566f-acbe-e938112d46d9",
                "validity": {"from": "1960-01-01", "to": None},
            },
            "user_key": "www.kolding.dk",
            "uuid": "341baf78-5602-48eb-9a79-3fbc20bc4240",
            "validity": {"from": "1960-01-01", "to": None},
            "value": "www.kolding.dk",
        },
        {
            "address_type": {
                "example": None,
                "name": "P-nummer",
                "scope": "PNUMBER",
                "user_key": "p-nummer",
                "uuid": "2e36f204-1bef-4165-bd9b-9c1981b3d240",
            },
            "href": None,
            "name": "1866728518",
            "org_unit": {
                "name": "Kolding Kommune",
                "user_key": "Kolding Kommune",
                "uuid": "f06ee470-9f17-566f-acbe-e938112d46d9",
                "validity": {"from": "1960-01-01", "to": None},
            },
            "user_key": "1866728518",
            "uuid": "5021c3bc-9433-47e6-897b-20aaa948ece2",
            "validity": {"from": "1960-01-01", "to": None},
            "value": "1866728518",
        },
        {
            "address_type": {
                "example": None,
                "name": "Returadresse",
                "scope": "DAR",
                "user_key": "AdressePostRetur",
                "uuid": "cf6d84c7-fa8b-4e47-b14a-65c0e9680b92",
            },
            "href": "https://www.openstreetmap.org/?mlon=9.48929996&mlat=55.4950218&zoom=16",
            "name": "Castenskjoldsvej 2, 2., 6000 Kolding",
            "org_unit": {
                "name": "Kolding Kommune",
                "user_key": "Kolding Kommune",
                "uuid": "f06ee470-9f17-566f-acbe-e938112d46d9",
                "validity": {"from": "1960-01-01", "to": None},
            },
            "user_key": "75fb0bed-d7b0-45d5-b56d-745c9cdbe1f6",
            "uuid": "8e1562ce-411e-442b-bf23-18f41436dba8",
            "validity": {"from": "1960-01-01", "to": None},
            "value": "75fb0bed-d7b0-45d5-b56d-745c9cdbe1f6",
        },
        {
            "address_type": {
                "example": None,
                "name": "Henvendelsessted",
                "scope": "DAR",
                "user_key": "AdresseHenvendelsessted",
                "uuid": "e23c50a6-2093-472a-ba4d-a4e97b681079",
            },
            "href": "https://www.openstreetmap.org/?mlon=9.48929996&mlat=55.4950218&zoom=16",
            "name": "Castenskjoldsvej 2, 2., 6000 Kolding",
            "org_unit": {
                "name": "Kolding Kommune",
                "user_key": "Kolding Kommune",
                "uuid": "f06ee470-9f17-566f-acbe-e938112d46d9",
                "validity": {"from": "1960-01-01", "to": None},
            },
            "user_key": "75fb0bed-d7b0-45d5-b56d-745c9cdbe1f6",
            "uuid": "c8c9d1e4-849b-4985-ac34-1578755bb8c1",
            "validity": {"from": "1960-01-01", "to": None},
            "value": "75fb0bed-d7b0-45d5-b56d-745c9cdbe1f6",
        },
        {
            "address_type": {
                "example": None,
                "name": "EAN-nummer",
                "scope": "EAN",
                "user_key": "EAN",
                "uuid": "6fc298c2-8bcc-4ec2-9457-490420d586a4",
            },
            "href": None,
            "name": "1224321145484",
            "org_unit": {
                "name": "Kolding Kommune",
                "user_key": "Kolding Kommune",
                "uuid": "f06ee470-9f17-566f-acbe-e938112d46d9",
                "validity": {"from": "1960-01-01", "to": None},
            },
            "user_key": "1224321145484",
            "uuid": "cc2ede77-baa5-4798-a865-2ddd5f3ff606",
            "validity": {"from": "1960-01-01", "to": None},
            "value": "1224321145484",
        },
        {
            "address_type": {
                "example": None,
                "name": "Postadresse",
                "scope": "DAR",
                "user_key": "AddressMailUnit",
                "uuid": "5260d4aa-e33b-48f7-ae3e-6074262cbdcf",
            },
            "href": "https://www.openstreetmap.org/?mlon=9.48929996&mlat=55.4950218&zoom=16",
            "name": "Castenskjoldsvej 2, 2., 6000 Kolding",
            "org_unit": {
                "name": "Kolding Kommune",
                "user_key": "Kolding Kommune",
                "uuid": "f06ee470-9f17-566f-acbe-e938112d46d9",
                "validity": {"from": "1960-01-01", "to": None},
            },
            "user_key": "75fb0bed-d7b0-45d5-b56d-745c9cdbe1f6",
            "uuid": "dd907dcd-d201-4bd7-9869-78b36aa675ab",
            "validity": {"from": "1960-01-01", "to": None},
            "value": "75fb0bed-d7b0-45d5-b56d-745c9cdbe1f6",
        },
    ]


def org_unit_engagements() -> List[dict]:
    """Get organisation engagement details from os2mo

    GET /service/o/ou/3b866d97-0b1f-48e0-8078-686d96f430b3/details/engagement

    Returns:
        List[dict]: A list of related engagement objects

    """

    return [
        {
            "engagement_type": {
                "example": None,
                "name": "Ansat",
                "scope": "TEXT",
                "user_key": "Ansat",
                "uuid": "8acc5743-044b-4c82-9bb9-4e572d82b524",
            },
            "fraction": None,
            "integration_data": {
                "Artificial import": '"c38a6883e2968040f1ca5c61796b8c749e65d3720f19c41de5a2d5b667a1c344"STOP_DUMMY'
            },
            "is_primary": None,
            "job_function": {
                "example": None,
                "name": "Specialkonsulent",
                "scope": "TEXT",
                "user_key": "Specialkonsulent",
                "uuid": "ff9e1efd-d799-4327-bcf0-cf4b2091b438",
            },
            "org_unit": {
                "name": "Kolding Kommune",
                "user_key": "Kolding Kommune",
                "uuid": "f06ee470-9f17-566f-acbe-e938112d46d9",
                "validity": {"from": "1960-01-01", "to": None},
            },
            "person": {
                "givenname": "Lykke Skytte",
                "name": "Lykke Skytte Hansen",
                "surname": "Hansen",
                "uuid": "eff3fca2-645c-4613-90ad-5fb47db47bc7",
            },
            "primary": {
                "example": None,
                "name": "Primær",
                "scope": "3000",
                "user_key": "primary",
                "uuid": "0644cd06-b84b-42e0-95fe-ce131c21fbe6",
            },
            "user_key": "-",
            "uuid": "b7e1ce81-f160-43ee-aac4-e416338e2a92",
            "validity": {"from": "1994-12-28", "to": None},
        },
        {
            "engagement_type": {
                "example": None,
                "name": "Ansat",
                "scope": "TEXT",
                "user_key": "Ansat",
                "uuid": "8acc5743-044b-4c82-9bb9-4e572d82b524",
            },
            "fraction": None,
            "integration_data": {
                "Artificial import": '"119e54957afe5ab123d2b055df01db0688625e7b01c96849c0bd167b37b9a511"STOP_DUMMY'
            },
            "is_primary": None,
            "job_function": {
                "example": None,
                "name": "Ressourcepædagog",
                "scope": "TEXT",
                "user_key": "Ressourcepædagog",
                "uuid": "38638313-d9e6-4e1d-aea6-67f5fce7a6b0",
            },
            "org_unit": {
                "name": "Kolding Kommune",
                "user_key": "Kolding Kommune",
                "uuid": "f06ee470-9f17-566f-acbe-e938112d46d9",
                "validity": {"from": "1960-01-01", "to": None},
            },
            "person": {
                "givenname": "Johannes Engmann Korsgård",
                "name": "Johannes Engmann Korsgård Maaløe",
                "surname": "Maaløe",
                "uuid": "be39de52-060a-4ae3-b705-ba46dd9b27a6",
            },
            "primary": {
                "example": None,
                "name": "Primær",
                "scope": "3000",
                "user_key": "primary",
                "uuid": "0644cd06-b84b-42e0-95fe-ce131c21fbe6",
            },
            "user_key": "-",
            "uuid": "be3bac37-034c-4626-8790-24a59df29edd",
            "validity": {"from": "2001-02-24", "to": None},
        },
        {
            "engagement_type": {
                "example": None,
                "name": "Ansat",
                "scope": "TEXT",
                "user_key": "Ansat",
                "uuid": "8acc5743-044b-4c82-9bb9-4e572d82b524",
            },
            "fraction": None,
            "integration_data": {
                "Artificial import": '"fa598ae55496acce06762eb366a3fb29d09f82c068a9da6ead193864b9471206"STOP_DUMMY'
            },
            "is_primary": None,
            "job_function": {
                "example": None,
                "name": "Teknisk Servicemedarb.",
                "scope": "TEXT",
                "user_key": "Teknisk Servicemedarb.",
                "uuid": "f0e22017-58a0-43fb-9662-f4847e466e85",
            },
            "org_unit": {
                "name": "Kolding Kommune",
                "user_key": "Kolding Kommune",
                "uuid": "f06ee470-9f17-566f-acbe-e938112d46d9",
                "validity": {"from": "1960-01-01", "to": None},
            },
            "person": {
                "givenname": "Christian Fregerslev",
                "name": "Christian Fregerslev Ulriksen",
                "surname": "Ulriksen",
                "uuid": "6037238b-a013-4520-86c8-b2ea15ee88d5",
            },
            "primary": {
                "example": None,
                "name": "Primær",
                "scope": "3000",
                "user_key": "primary",
                "uuid": "0644cd06-b84b-42e0-95fe-ce131c21fbe6",
            },
            "user_key": "-",
            "uuid": "c5c2e3e7-1fc8-4a3d-96b9-925e6fc81672",
            "validity": {"from": "1968-10-15", "to": None},
        },
    ]


def org_unit_managers() -> list:
    """Get organisation manager details from os2mo

    GET /service/o/ou/3b866d97-0b1f-48e0-8078-686d96f430b3/details/manager

    Returns:
        List[dict]: A list of related manager objects

    """

    return [
        {
            "address": [],
            "manager_level": {
                "example": None,
                "name": "Niveau 4",
                "scope": "TEXT",
                "user_key": "Niveau 4",
                "uuid": "72d98bd0-418f-4786-b38b-194200d70ab3",
            },
            "manager_type": {
                "example": None,
                "name": "Direktør",
                "scope": "TEXT",
                "user_key": "Direktør",
                "uuid": "8762f1d2-5180-4c59-92b5-9f334b018cab",
            },
            "org_unit": {
                "name": "Gudme børnehus",
                "user_key": "Gudme børnehus",
                "uuid": "0cb0c26b-5067-5701-b2f2-9718939a2758",
                "validity": {"from": "1960-01-01", "to": None},
            },
            "person": {
                "givenname": "Peter Behrens",
                "name": "Peter Behrens Høgfeldt",
                "surname": "Høgfeldt",
                "uuid": "84f4536f-52d4-4229-a675-9a92d71be79c",
            },
            "responsibility": [
                {
                    "example": None,
                    "name": "Personale: MUS-kompetence",
                    "scope": "TEXT",
                    "user_key": "Personale: MUS-kompetence",
                    "uuid": "d2052939-c1f7-4418-969b-ba70064265dc",
                },
                {
                    "example": None,
                    "name": "Personale: Sygefravær",
                    "scope": "TEXT",
                    "user_key": "Personale: Sygefravær",
                    "uuid": "84abcae9-5130-4d6a-875b-8e4742eea9d1",
                },
                {
                    "example": None,
                    "name": "Personale: ansættelse/afskedigelse",
                    "scope": "TEXT",
                    "user_key": "Personale: ansættelse/afskedigelse",
                    "uuid": "e0668bc9-9df5-4a58-b960-b2254724e3b1",
                },
            ],
            "user_key": "b781d5fb-621d-41b0-be57-54524972e61a",
            "uuid": "b781d5fb-621d-41b0-be57-54524972e61a",
            "validity": {"from": "1992-09-09", "to": None},
        }
    ]


def org_unit_associations() -> list:
    """Get organisation association details from os2mo

    GET /service/o/ou/3b866d97-0b1f-48e0-8078-686d96f430b3/details/association

    Returns:
        List[dict]: A list of related association objects

    """

    return [
        {
            "association_type": {
                "example": None,
                "name": "Næstformand",
                "scope": "TEXT",
                "user_key": "Næstformand",
                "uuid": "dcfb14ee-3a0a-40fa-989c-94e6931af0bd",
            },
            "org_unit": {
                "name": "Gudme børnehus",
                "user_key": "Gudme børnehus",
                "uuid": "0cb0c26b-5067-5701-b2f2-9718939a2758",
                "validity": {"from": "1960-01-01", "to": None},
            },
            "person": {
                "givenname": "Hans Pie",
                "name": "Hans Pie Rasmussen",
                "surname": "Rasmussen",
                "uuid": "1acb3999-423a-48c4-9ef8-ba4452929d7a",
            },
            "primary": None,
            "user_key": "fc2ce78b-bd79-4ec0-b938-d0219d8bb184",
            "uuid": "fc2ce78b-bd79-4ec0-b938-d0219d8bb184",
            "validity": {"from": "2009-02-12", "to": None},
        }
    ]


def single_employee() -> dict:
    """Get a single employee from os2mo

    GET /service/o/3b866d97-0b1f-48e0-8078-686d96f430b3/e/?limit=1

    Returns:
        dict: An os2mo employees object

    """

    return {
        "items": [
            {
                "givenname": "Aage Christensen Moesgård",
                "name": "Aage Christensen Moesgård Egeberg",
                "surname": "Egeberg",
                "uuid": "64c85f9f-ba89-407f-bbb2-7f524ce6a66e",
            }
        ],
        "offset": 0,
        "total": 897,
    }


def several_employees() -> dict:
    """Get several (limit=4) employee from os2mo

    GET /service/o/3b866d97-0b1f-48e0-8078-686d96f430b3/e/?limit=4

    Returns:
        dict: An os2mo employees object

    """

    return {
        "items": [
            {
                "givenname": "Aage Bruun Lund",
                "name": "Aage Bruun Lund Happe",
                "surname": "Happe",
                "uuid": "26d43382-ce39-4772-aee5-c711732ca345",
            },
            {
                "givenname": "Aage",
                "name": "Aage Foghsgaard",
                "surname": "Foghsgaard",
                "uuid": "60fdff44-658f-45f0-842f-fe2c5b1b074f",
            },
            {
                "givenname": "Aage Christensen Moesgård",
                "name": "Aage Christensen Moesgård Egeberg",
                "surname": "Egeberg",
                "uuid": "64c85f9f-ba89-407f-bbb2-7f524ce6a66e",
            },
            {
                "givenname": "Aage Bach",
                "name": "Aage Bach Klarskov",
                "surname": "Klarskov",
                "uuid": "c6f61ee9-b902-492c-b4c8-76df54088cc9",
            },
        ],
        "offset": 0,
        "total": 897,
    }


def employee_addresses() -> List[dict]:
    """Get address types for a given employee

    GET /service/e/64c85f9f-ba89-407f-bbb2-7f524ce6a66e/details/address

    Returns:
        List[dict]: A list of related address type objects

    """

    return [
        {
            "address_type": {
                "example": None,
                "name": "Email",
                "scope": "EMAIL",
                "user_key": "EmailEmployee",
                "uuid": "c4b75285-c0b1-4c38-a280-0c7a575adc27",
            },
            "href": "mailto:annb@svendborg.dk",
            "name": "annb@svendborg.dk",
            "person": {
                "givenname": "Ann Theibel",
                "name": "Ann Theibel Bech",
                "surname": "Bech",
                "uuid": "5568a304-4aaf-4011-8f1b-df1717c0d832",
            },
            "user_key": "annb@svendborg.dk",
            "uuid": "2cde303f-eeb2-4501-a338-4c92e7f4fecd",
            "validity": {"from": "1961-05-25", "to": None},
            "value": "annb@svendborg.dk",
        },
        {
            "address_type": {
                "example": None,
                "name": "Telefon",
                "scope": "PHONE",
                "user_key": "PhoneEmployee",
                "uuid": "e2dd63e3-3408-4c3a-9b4f-4fd8f3c48e4d",
            },
            "href": "tel:+4511681745",
            "name": "+4511681745",
            "person": {
                "givenname": "Ann Theibel",
                "name": "Ann Theibel Bech",
                "surname": "Bech",
                "uuid": "5568a304-4aaf-4011-8f1b-df1717c0d832",
            },
            "user_key": "+4511681745",
            "uuid": "69086cd2-c944-4f94-9346-72a1b5db55c7",
            "validity": {"from": "1961-05-25", "to": None},
            "value": "+4511681745",
            "visibility": {
                "example": None,
                "name": "Hemmelig",
                "scope": "SECRET",
                "user_key": "Hemmelig",
                "uuid": "ed17f9bc-f9fd-413d-8eaa-2d3eff367009",
            },
        },
        {
            "address_type": {
                "example": None,
                "name": "Postadresse",
                "scope": "DAR",
                "user_key": "AdressePostEmployee",
                "uuid": "0c91b03b-8c84-4b13-922a-4552cc3e61e0",
            },
            "href": "https://www.openstreetmap.org/?mlon=10.61293469&mlat=55.05887822&zoom=16",
            "name": "Frederiksgade 11E, 5700 Svendborg",
            "person": {
                "givenname": "Ann Theibel",
                "name": "Ann Theibel Bech",
                "surname": "Bech",
                "uuid": "5568a304-4aaf-4011-8f1b-df1717c0d832",
            },
            "user_key": "Frederiksgade 11E, 5700 Svendborg",
            "uuid": "ba0b4348-4291-445d-9c0d-06464be50d00",
            "validity": {"from": "1961-05-25", "to": None},
            "value": "c059e51f-c608-4282-89d5-599d8ec0272b",
        },
    ]


def employee_engagements() -> List[dict]:
    """Get an employees engagements

    GET /service/e/64c85f9f-ba89-407f-bbb2-7f524ce6a66e/details/engagement

    Returns:
        List[dict]: A list of related engagement objects

    """

    return [
        {
            "engagement_type": {
                "example": None,
                "name": "Ansat",
                "scope": "TEXT",
                "user_key": "Ansat",
                "uuid": "282e46e0-bc5e-4fdf-b10b-8e346a6358de",
            },
            "fraction": None,
            "integration_data": {
                "Artificial import": '"256d6e79a4b2542bcb1ac42a8ffbbad3897df166c41f1fe3e1b73fc1b3013ab3"STOP_DUMMY'
            },
            "job_function": {
                "example": None,
                "name": "Timelønnet lærer",
                "scope": "TEXT",
                "user_key": "Timelønnet lærer",
                "uuid": "74bfe22b-6334-4ac8-8208-f0bfd134772f",
            },
            "org_unit": {
                "name": "Svendborg Kommune",
                "user_key": "Svendborg Kommune",
                "uuid": "f06ee470-9f17-566f-acbe-e938112d46d9",
                "validity": {"from": "1960-01-01", "to": None},
            },
            "person": {
                "givenname": "Jens",
                "name": "Jens Lausen",
                "surname": "Lausen",
                "uuid": "43c1e60e-6ab4-4ad7-b943-ae669fb217a3",
            },
            "primary": None,
            "user_key": "-",
            "uuid": "f5edba5b-d057-47b2-af57-d1c0b1db47d9",
            "validity": {"from": "1978-10-23", "to": None},
        }
    ]


def employee_managers() -> List[dict]:
    """Get an employees manager roles

    GET /service/e/64c85f9f-ba89-407f-bbb2-7f524ce6a66e/details/manager

    Returns:
        List[dict]: A list of related manager objects

    """

    return [
        {
            "address": [],
            "manager_level": {
                "example": None,
                "name": "Lederniveau",
                "scope": "TEXT",
                "user_key": "Lederniveau",
                "uuid": "fa5717e4-9400-43ff-8f3e-de8858ab6816",
            },
            "manager_type": {
                "example": None,
                "name": "Direktør",
                "scope": "TEXT",
                "user_key": "Direktør",
                "uuid": "6896b73c-ebed-44d5-973a-7cf3dcc6a254",
            },
            "org_unit": {
                "name": "Direktør område Anne Vang",
                "user_key": "DIRAA",
                "uuid": "d9ccd8f8-7c7c-4788-80c0-cfc3dd7ff6ce",
                "validity": {"from": "2011-05-02", "to": None},
            },
            "person": {
                "givenname": "Anne Vang ",
                "name": "Anne Vang  Rasmussen",
                "surname": "Rasmussen",
                "uuid": "c68bbab9-5699-4498-8339-3528505f7e4a",
            },
            "responsibility": [
                {
                    "example": None,
                    "name": "Beredskabsledelse",
                    "scope": "TEXT",
                    "user_key": "Beredskabsledelse",
                    "uuid": "74398697-d205-45e5-b4e2-bc04afdfb0ff",
                },
                {
                    "example": None,
                    "name": "Personale: ansættelse/afskedigelse",
                    "scope": "TEXT",
                    "user_key": "Personale: ansættelse/afskedigelse",
                    "uuid": "516a18f2-8a1e-44a9-9daf-84a94f752358",
                },
            ],
            "user_key": "f621459a-3478-4817-b5b4-ae4cfc71d647",
            "uuid": "f621459a-3478-4817-b5b4-ae4cfc71d647",
            "validity": {"from": "2012-05-29", "to": None},
        }
    ]


def employee_associations() -> List[dict]:
    """Get an employees associations

    GET /service/e/64c85f9f-ba89-407f-bbb2-7f524ce6a66e/details/association

    Returns:
        List[dict]: A list of related association objects

    """

    return [
        {
            "association_type": {
                "example": None,
                "name": "Ansat",
                "scope": "TEXT",
                "user_key": "Ansat",
                "uuid": "56e1214a-330f-4592-89f3-ae3ee8d5b2e6",
            },
            "org_unit": {
                "name": "Byg",
                "user_key": "Byg",
                "uuid": "6e95168a-82a5-40a7-b533-8a771c2f1fbb",
                "validity": {"from": "2017-09-01", "to": None},
            },
            "person": {
                "givenname": "Dorte Louise ",
                "name": "Dorte Louise  Virklund",
                "surname": "Virklund",
                "uuid": "da0d838e-cd16-4496-b005-eb85ef00028f",
            },
            "primary": None,
            "user_key": "a454e3c7-5ad6-49ab-b3bc-d315304524ac",
            "uuid": "a454e3c7-5ad6-49ab-b3bc-d315304524ac",
            "validity": {"from": "2002-12-31", "to": None},
        },
        {
            "association_type": {
                "example": None,
                "name": "Medlem",
                "scope": "TEXT",
                "user_key": "Medlem",
                "uuid": "2a138ce9-888b-4c3c-847a-7b3941ee8baa",
            },
            "org_unit": {
                "name": "L-MED Center for By Erhverv og Miljø",
                "user_key": "25448337-42e4-459f-8bdf-0e3da90a58f0",
                "uuid": "25448337-42e4-459f-8bdf-0e3da90a58f0",
                "validity": {"from": "1900-01-01", "to": None},
            },
            "person": {
                "givenname": "Dorte Louise ",
                "name": "Dorte Louise  Virklund",
                "surname": "Virklund",
                "uuid": "da0d838e-cd16-4496-b005-eb85ef00028f",
            },
            "primary": None,
            "user_key": "f5b2d951-9628-4245-ae69-8c1822887fb6",
            "uuid": "f5b2d951-9628-4245-ae69-8c1822887fb6",
            "validity": {"from": "2018-01-01", "to": None},
        },
    ]


def org_unit_vacant_managers() -> list:
    """Get a list of vacant manager positions

    GET /service/ou/2665d8e0-435b-5bb6-a550-f275692984ef/details/manager

    Essentially this is just the organisation manager relations
    without an attached `person`.

    Returns:
        List[dict]: A list of vacant manager objects

    """

    return [
        {
            "address": [],
            "manager_level": {
                "example": None,
                "name": "Niveau 4",
                "scope": "TEXT",
                "user_key": "Niveau 4",
                "uuid": "9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c",
            },
            "manager_type": {
                "example": None,
                "name": "Direktør",
                "scope": "TEXT",
                "user_key": "Direktør",
                "uuid": "267e5e49-3abd-49df-9bd9-38d41d2294ff",
            },
            "org_unit": {
                "name": "Skoler og børnehaver",
                "user_key": "Skoler og børnehaver",
                "uuid": "2665d8e0-435b-5bb6-a550-f275692984ef",
                "validity": {"from": "1960-01-01", "to": None},
            },
            "person": None,
            "responsibility": [
                {
                    "example": None,
                    "name": "Beredskabsledelse",
                    "scope": "TEXT",
                    "user_key": "Beredskabsledelse",
                    "uuid": "0bbe4518-27a0-46ba-87b1-f20f1bcfe56b",
                },
                {
                    "example": None,
                    "name": "Personale: ansættelse/afskedigelse",
                    "scope": "TEXT",
                    "user_key": "Personale: ansættelse/afskedigelse",
                    "uuid": "2f4f5cbc-35bd-4ee1-a220-5778036a15cd",
                },
                {
                    "example": None,
                    "name": "Personale: øvrige administrative opgaver",
                    "scope": "TEXT",
                    "user_key": "Personale: øvrige administrative opgaver",
                    "uuid": "bc15cd6c-81f9-49f6-b831-7e832673e5fd",
                },
            ],
            "user_key": "220c2015-1da8-4850-9c0e-78ed4947f540",
            "uuid": "220c2015-1da8-4850-9c0e-78ed4947f540",
            "validity": {"from": "2020-01-31", "to": None},
        }
    ]
