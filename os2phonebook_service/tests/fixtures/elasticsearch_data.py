# Fixtures
# These fixtures simulate the content returned
# by the actual Elasticsearch client
# The given examples should work 1:1 in a populated datastore


def all_org_units_from_elasticsearch() -> dict:
    """Search for 62 org units without any search arguments

    GET /org_units/_search

    {
        "size": 62,
        "query": {
            "match_all": {}
        }
    }

    Returns:
        dict: Result object from Elasticsearch

    """

    return {
        "took": 2,
        "timed_out": False,
        "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0},
        "hits": {
            "total": {"value": 62, "relation": "eq"},
            "max_score": 1.0,
            "hits": [
                {
                    "_index": "org_units",
                    "_type": "_doc",
                    "_id": "f06ee470-9f17-566f-acbe-e938112d46d9",
                    "_score": 1.0,
                    "_source": {
                        "parent": None,
                        "name": "Kolding Kommune",
                        "uuid": "f06ee470-9f17-566f-acbe-e938112d46d9",
                    },
                },
                {
                    "_index": "org_units",
                    "_type": "_doc",
                    "_id": "7a8e45f7-4de0-44c8-990f-43c0565ee505",
                    "_score": 1.0,
                    "_source": {
                        "parent": "f06ee470-9f17-566f-acbe-e938112d46d9",
                        "name": "Skole og Børn",
                        "uuid": "7a8e45f7-4de0-44c8-990f-43c0565ee505",
                    },
                },
                {
                    "_index": "org_units",
                    "_type": "_doc",
                    "_id": "2665d8e0-435b-5bb6-a550-f275692984ef",
                    "_score": 1.0,
                    "_source": {
                        "parent": "7a8e45f7-4de0-44c8-990f-43c0565ee505",
                        "name": "Skoler og børnehaver",
                        "uuid": "2665d8e0-435b-5bb6-a550-f275692984ef",
                    },
                },
                {
                    "_index": "org_units",
                    "_type": "_doc",
                    "_id": "5cb38a3c-cacd-5d54-9eb3-88eae2baba1b",
                    "_score": 1.0,
                    "_source": {
                        "parent": "2665d8e0-435b-5bb6-a550-f275692984ef",
                        "name": "Vamdrup skole",
                        "uuid": "5cb38a3c-cacd-5d54-9eb3-88eae2baba1b",
                    },
                },
                {
                    "_index": "org_units",
                    "_type": "_doc",
                    "_id": "327301c2-fdab-5773-9357-d0df0548258e",
                    "_score": 1.0,
                    "_source": {
                        "parent": "2665d8e0-435b-5bb6-a550-f275692984ef",
                        "name": "Christiansfeld børnehus",
                        "uuid": "327301c2-fdab-5773-9357-d0df0548258e",
                    },
                },
                {
                    "_index": "org_units",
                    "_type": "_doc",
                    "_id": "1caba8d9-6b9f-506b-b845-9a8c4f5b8a03",
                    "_score": 1.0,
                    "_source": {
                        "parent": "2665d8e0-435b-5bb6-a550-f275692984ef",
                        "name": "Jordrup børnehus",
                        "uuid": "1caba8d9-6b9f-506b-b845-9a8c4f5b8a03",
                    },
                },
                {
                    "_index": "org_units",
                    "_type": "_doc",
                    "_id": "7133da92-e624-56c9-8e23-bac319a537e1",
                    "_score": 1.0,
                    "_source": {
                        "parent": "1caba8d9-6b9f-506b-b845-9a8c4f5b8a03",
                        "name": "Administration",
                        "uuid": "7133da92-e624-56c9-8e23-bac319a537e1",
                    },
                },
                {
                    "_index": "org_units",
                    "_type": "_doc",
                    "_id": "23a2ace2-52ca-458d-bead-d1a42080579f",
                    "_score": 1.0,
                    "_source": {
                        "parent": "f06ee470-9f17-566f-acbe-e938112d46d9",
                        "name": "Teknik og Miljø",
                        "uuid": "23a2ace2-52ca-458d-bead-d1a42080579f",
                    },
                },
                {
                    "_index": "org_units",
                    "_type": "_doc",
                    "_id": "b6c11152-0645-4712-a207-ba2c53b391ab",
                    "_score": 1.0,
                    "_source": {
                        "parent": "f06ee470-9f17-566f-acbe-e938112d46d9",
                        "name": "Borgmesterens Afdeling",
                        "uuid": "b6c11152-0645-4712-a207-ba2c53b391ab",
                    },
                },
                {
                    "_index": "org_units",
                    "_type": "_doc",
                    "_id": "f1c20ee2-ecbb-4b74-b91c-66ef9831c5cd",
                    "_score": 1.0,
                    "_source": {
                        "parent": "b6c11152-0645-4712-a207-ba2c53b391ab",
                        "name": "Byudvikling",
                        "uuid": "f1c20ee2-ecbb-4b74-b91c-66ef9831c5cd",
                    },
                },
            ],
        },
    }


def one_unit_from_elasticsearch() -> dict:
    """Search for 1 org unit without any search arguments

    GET /org_units/_search

    {
        "size": 1,
        "query": {
            "match_all": {
            }
        }
    }

    Returns:
        dict: Result object from Elasticsearch

    """

    return {
        "_index": "org_units",
        "_type": "_doc",
        "_id": "1f06ed67-aa6e-4bbc-96d9-2f262b9202b5",
        "_version": 1,
        "_seq_no": 46,
        "_primary_term": 1,
        "found": True,
        "_source": {
            "uuid": "1f06ed67-aa6e-4bbc-96d9-2f262b9202b5",
            "name": "Budget og Planlægning",
            "addresses": {
                "DAR": [
                    {
                        "description": "Postadresse",
                        "value": "Kildeparken 64A, Seest, 6000 Kolding",
                    },
                    {
                        "description": "Returadresse",
                        "value": "Kildeparken 64A, Seest, 6000 Kolding",
                    },
                    {
                        "description": "Henvendelsessted",
                        "value": "Kildeparken 64A, Seest, 6000 Kolding",
                    },
                ],
                "PHONE": [],
                "EMAIL": [
                    {
                        "description": "Email",
                        "value": "Budget_og_Planlægning@kolding.dk",
                    }
                ],
                "EAN": [{"description": "EAN-nummer", "value": "2617445301464"}],
                "PNUMBER": [{"description": "P-nummer", "value": "5424825851"}],
                "WWW": [],
            },
            "engagements": [
                {
                    "title": "Lærer/Overlærer",
                    "name": "Qais Udstad Gade",
                    "uuid": "8441b33b-ca64-403d-93d3-44357a05c669",
                },
                {
                    "title": "Udviklingskonsulent",
                    "name": "Elisabeth Goldberg",
                    "uuid": "929bd71f-452a-4633-ace2-3416e16e37c5",
                },
                {
                    "title": "Lønkonsulent",
                    "name": "Marinus Soto",
                    "uuid": "c5a4aaf7-920b-456b-a4de-3ae1741e36fd",
                },
                {
                    "title": "Lønkonsulent",
                    "name": "Jamilla Jensen",
                    "uuid": "1fa0810d-eaf7-4442-9a5d-2df8ce891917",
                },
                {
                    "title": "Bogopsætter",
                    "name": "Magnus Alslev Munck",
                    "uuid": "7187a259-d266-4500-9f93-2ab8b0b0051d",
                },
                {
                    "title": "Lærer/Overlærer",
                    "name": "Jan Elkjær Winther Nielsen",
                    "uuid": "f16eee45-d96a-4efb-bd17-667d1795e13d",
                },
                {
                    "title": "Støttepædagog",
                    "name": "Abelone Thomsen",
                    "uuid": "c8da0668-ac70-44c4-8e24-3badfdc43eaf",
                },
                {
                    "title": "Ergoterapeut",
                    "name": "Nils Ingerslev Wigh-Thomsen",
                    "uuid": "41512f57-f013-4f29-880f-6a514d16a6b3",
                },
                {
                    "title": "Udviklingskonsulent",
                    "name": "Viola Bårris Jacobsen",
                    "uuid": "461d4404-8b8f-4d42-bcc3-28bb83aafb03",
                },
            ],
            "associations": [
                {
                    "title": "Medarbejder",
                    "name": "Mathilde Olsen",
                    "uuid": "7faf0a01-85ff-42eb-9b21-0101b1de5685",
                },
                {
                    "title": "Formand",
                    "name": "Mersiha Lund Bryant",
                    "uuid": "ad4caf7d-01ad-4b0d-92a8-5a3f6f0e7d14",
                },
                {
                    "title": "Leder",
                    "name": "Mohammad Sørensen",
                    "uuid": "4ef20524-e1a2-47e9-86fe-126a067d814c",
                },
                {
                    "title": "Formand",
                    "name": "Birthe Bjerregaard Rasmussen",
                    "uuid": "b0317784-3a57-4318-b7b5-a47146cd9cc3",
                },
            ],
            "management": [
                {
                    "title": "Direktør",
                    "name": "Jan Elkjær Winther Nielsen",
                    "uuid": "f16eee45-d96a-4efb-bd17-667d1795e13d",
                }
            ],
            "parent": "b6c11152-0645-4712-a207-ba2c53b391ab",
        },
    }


def one_employee_from_elasticsearch() -> dict:
    """Get employee by uuid

    GET /employees/_doc/f16eee45-d96a-4efb-bd17-667d1795e13d

    Returns:
        dict: Result object from Elasticsearch

    """

    return {
        "_index": "employees",
        "_type": "_doc",
        "_id": "f16eee45-d96a-4efb-bd17-667d1795e13d",
        "_version": 1,
        "_seq_no": 341,
        "_primary_term": 1,
        "found": True,
        "_source": {
            "givenname": "Jan Elkjær Winther",
            "name": "Jan Elkjær Winther Nielsen",
            "surname": "Nielsen",
            "uuid": "f16eee45-d96a-4efb-bd17-667d1795e13d",
            "engagements": [
                {
                    "title": "Lærer/Overlærer",
                    "name": "Budget og Planlægning",
                    "uuid": "1f06ed67-aa6e-4bbc-96d9-2f262b9202b5",
                }
            ],
            "associations": [],
            "management": [
                {
                    "title": "Direktør",
                    "name": "Budget og Planlægning",
                    "uuid": "1f06ed67-aa6e-4bbc-96d9-2f262b9202b5",
                }
            ],
            "addresses": {
                "DAR": [
                    {
                        "description": "Postadresse",
                        "value": "Tøndervej 30, Bastrup, 6580 Vamdrup",
                    }
                ],
                "PHONE": [{"description": "Telefon", "value": "64535362"}],
                "EMAIL": [{"description": "Email", "value": "jann@kolding.dk"}],
                "EAN": [],
                "PNUMBER": [],
                "WWW": [],
            },
        },
    }


def no_matches_from_elasticsearch() -> dict:
    """Search employee with non-existing identifier

    GET /employees/_search

    {
        "size": 1,
        "query": {
            "match": {
                "uuid": "sdfsdfsdf"
            }
        }
    }

    Returns:
        dict: Result object from Elasticsearch

    """

    return {
        "took": 0,
        "timed_out": False,
        "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0},
        "hits": {
            "total": {"value": 0, "relation": "eq"},
            "max_score": None,
            "hits": [],
        },
    }


def one_employee_by_name_from_elasticsearch() -> dict:
    """Search employee with non-existing identifier

    GET /employees/_search

    {
        "size": 1,
        "query": {
            "match": {
                "name": "Anne Yassen"
            }
        }
    }

    Returns:
        dict: Result object from Elasticsearch

    """

    return {
        "took": 2,
        "timed_out": False,
        "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0},
        "hits": {
            "total": {"value": 1, "relation": "eq"},
            "max_score": 12.183924,
            "hits": [
                {
                    "_index": "employees",
                    "_type": "_doc",
                    "_id": "048c045c-02c4-45ab-a43f-bda6ac99448e",
                    "_score": 12.183924,
                    "_source": {
                        "addresses": {
                            "PHONE": [{"description": "Telefon", "value": "61325558"}]
                        },
                        "name": "Anne Yassen",
                        "uuid": "048c045c-02c4-45ab-a43f-bda6ac99448e",
                    },
                }
            ],
        },
    }
