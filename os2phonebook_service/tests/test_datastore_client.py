import pytest
import inspect
from unittest import mock
from elasticsearch import Elasticsearch

from os2phonebook.exceptions import InvalidSearchType
from os2phonebook.datastore import create_connection, DataStore

from tests.fixtures.elasticsearch_data import (
    all_org_units_from_elasticsearch,
    one_employee_from_elasticsearch,
    no_matches_from_elasticsearch,
)


@pytest.fixture
def db() -> DataStore:
    """Create DataStore client instance"""

    connection = create_connection(host="testhost", port=9090)
    return DataStore(connection)


def test_connection(db):
    """Should return an instance of the Elasticsearch client"""

    connection = create_connection(host="testhost", port=9090)

    assert isinstance(connection, Elasticsearch)


@mock.patch("os2phonebook.datastore.Elasticsearch.search")
def test_get_all_org_units(mock_search, db):
    """Should return a list of org unit dictionaries"""

    mock_search.return_value = all_org_units_from_elasticsearch()

    results = db.get_all_org_units()

    expected = {
        "uuid": "f06ee470-9f17-566f-acbe-e938112d46d9",
        "name": "Kolding Kommune",
        "parent": None,
    }

    assert results[0] == expected


@mock.patch("os2phonebook.datastore.Elasticsearch.search")
def test_get_all_org_units_no_results(mock_search, db):
    """Should return an empty list"""

    mock_search.return_value = no_matches_from_elasticsearch()

    results = db.get_all_org_units()

    assert results == []


def test_map_contains_query_methods(db):
    """The map should not be missing any query methods"""

    missing_query_methods = 0

    for search_type in db.search_type_map.values():
        if "query_method" not in search_type:
            missing_query_methods = +1
            continue

        query_method = search_type["query_method"]

        if not hasattr(db, query_method):
            missing_query_methods = +1

    expected_missing_methods = 0

    assert missing_query_methods == expected_missing_methods


@mock.patch("os2phonebook.datastore.Elasticsearch.get")
def test_get_employee(mock_result, db):
    """Should return an employee with the (mocked) corresponding uuid"""

    mock_result.return_value = one_employee_from_elasticsearch()

    uuid = "f16eee45-d96a-4efb-bd17-667d1795e13d"

    employee = db.get_employee(uuid)

    employee_uuid = employee["uuid"]

    assert employee_uuid == uuid


@mock.patch("os2phonebook.datastore.Elasticsearch.search")
def test_get_employee_total_size_type(mock_search, db):
    """Should return the total size as an integer"""

    mock_search.return_value = all_org_units_from_elasticsearch()

    index = "org_units"
    total_size = db.get_size(index)

    assert isinstance(total_size, int)


@mock.patch("os2phonebook.datastore.Elasticsearch.search")
def test_get_employee_total_size_value(mock_search, db):
    """Should return the total size value (fixture contains 62)"""

    mock_search.return_value = all_org_units_from_elasticsearch()

    index = "org_units"

    total_size = db.get_size(index)

    assert total_size == 62


def test_query_method_interface(db):
    """Passing a non-string type should raise TypeError"""

    search_type = 15

    with pytest.raises(TypeError):
        db.get_query_method(search_type)


def test_query_method_invalid_search_type(db):
    """A non-specified search type should raise InvalidSearchType"""

    unknown_search_type = "spaceship_types_by_name"

    with pytest.raises(InvalidSearchType):
        db.get_query_method(unknown_search_type)


def test_query_method_missing(db):
    """Resolved query method should be an actual instance method"""

    employee_by_name = "employee_by_name"

    query_method = db.get_query_method(employee_by_name)

    assert inspect.ismethod(query_method)


def test_query_match(db):
    """Should return a `match` query with the given arguments"""

    query = db._query_match(
        search_field="name",
        search_value="Jean Luc Picard",
        size=10,
        source_filter=["uuid", "name", "addresses.PHONE"],
    )

    expected = {
        "size": 10,
        "_source": {"includes": ["uuid", "name", "addresses.PHONE"]},
        "query": {"match": {"name": "Jean Luc Picard"}},
    }

    assert query == expected


def test_query_match_phrase_prefix(db):
    """Should return a `match_phrase_prefix` query with the given arguments"""

    query = db._query_match_phrase_prefix(
        search_field="name",
        search_value="Jean Luc Picard",
        size=15,
        source_filter=["uuid", "name"],
    )

    expected_query = {
        "size": 15,
        "_source": {"includes": ["uuid", "name"]},
        "query": {"match_phrase_prefix": {"name": "Jean Luc Picard"}},
    }

    assert query == expected_query


def test_query_for_employee_by_name(db):
    """Should return a `multi_match` query with the given arguments"""

    query = db.query_for_employee_by_name(
        name="Diana Troy", fuzzy_search=False
    )

    expected_index = "employees"
    expected_query = {
        "_source": {"includes": ["uuid", "name", "addresses.PHONE"]},
        "query": {
            "multi_match": {
                "query": "Diana Troy",
                "type": "phrase_prefix",
                "fields": ["surname", "name"],
            }
        },
    }

    expected = (expected_index, expected_query)

    assert query == expected


def test_fuzzy_query_for_employee_by_name(db):
    """Should return a `bool` query with the given arguments"""

    query = db.query_for_employee_by_name(name="Diana Troy", fuzzy_search=True)

    expected_index = "employees"
    expected_query = {
        "_source": {"includes": ["uuid", "name", "addresses.PHONE"]},
        "query": {
            "bool": {
                "must": [{"match": {"name": "Diana Troy"}}],
                "should": [{"match_phrase_prefix": {"surname": "Troy"}}],
            }
        },
    }

    expected = (expected_index, expected_query)

    assert query == expected


def test_query_for_employee_by_phone(db):
    """Should return a `match` query with the given arguments"""

    query = db.query_for_employee_by_phone(
        phone_number="2233", fuzzy_search=False
    )

    expected_index = "employees"
    expected_query = {
        "size": 15,
        "_source": {"includes": ["uuid", "name", "addresses.PHONE"]},
        "query": {"match": {"addresses.PHONE.value": "2233"}},
    }

    expected = (expected_index, expected_query)

    assert query == expected


def test_fuzzy_query_for_employee_by_phone(db):
    """Should return a `match_phrase_prefix` query with the given arguments"""

    query = db.query_for_employee_by_phone(
        phone_number="3344", fuzzy_search=True
    )

    expected_index = "employees"
    expected_query = {
        "size": 15,
        "_source": {"includes": ["uuid", "name", "addresses.PHONE"]},
        "query": {"match_phrase_prefix": {"addresses.PHONE.value": "3344"}},
    }

    expected = (expected_index, expected_query)

    assert query == expected


def test_query_for_employee_by_email(db):
    """Should return a `match_phrase_prefix` query with the given arguments"""

    query = db.query_for_employee_by_email(
        email_address="regular@example.com", fuzzy_search=False
    )

    expected_index = "employees"
    expected_query = {
        "size": 15,
        "_source": {"includes": ["uuid", "name", "addresses.EMAIL"]},
        "query": {
            "match_phrase_prefix": {
                "addresses.EMAIL.value": "regular@example.com"
            }
        },
    }

    expected = (expected_index, expected_query)

    assert query == expected


def test_fuzzy_query_for_employee_by_email(db):
    """Should return a `match_phrase_prefix` query with the given arguments"""

    query = db.query_for_employee_by_email(
        email_address="fuzzy@example.com", fuzzy_search=True
    )

    expected_index = "employees"
    expected_query = {
        "size": 15,
        "_source": {"includes": ["uuid", "name", "addresses.EMAIL"]},
        "query": {
            "match_phrase_prefix": {
                "addresses.EMAIL.value": "fuzzy@example.com"
            }
        },
    }

    expected = (expected_index, expected_query)

    assert query == expected


def test_query_for_employee_by_engagement(db):
    """Should return a `match_phrase_prefix` query with the given arguments"""

    query = db.query_for_employee_by_engagement(
        engagement="Bridge officer", fuzzy_search=False
    )

    expected_index = "employees"
    expected_query = {
        "size": 15,
        "_source": {"includes": ["uuid", "name", "engagements"]},
        "query": {
            "match_phrase_prefix": {"engagements.title": "Bridge officer"}
        },
    }

    expected = (expected_index, expected_query)

    assert query == expected


def test_fuzzy_query_for_employee_by_engagement(db):
    """Should return a `match_phrase_prefix` query with the given arguments"""

    query = db.query_for_employee_by_engagement(
        engagement="Bridge officer", fuzzy_search=True
    )

    expected_index = "employees"
    expected_query = {
        "size": 15,
        "_source": {"includes": ["uuid", "name", "engagements"]},
        "query": {
            "match_phrase_prefix": {"engagements.title": "Bridge officer"}
        },
    }

    expected = (expected_index, expected_query)

    assert query == expected


def test_query_for_org_unit_by_name(db):
    """Should return a `match_phrase_prefix` query with the given arguments"""

    query = db.query_for_org_unit_by_name(
        name="Engineering", fuzzy_search=False
    )

    expected_index = "org_units"
    expected_query = {
        "size": 15,
        "_source": {"includes": ["uuid", "name", "addresses"]},
        "query": {"match_phrase_prefix": {"name": "Engineering"}},
    }

    expected = (expected_index, expected_query)

    assert query == expected


def test_fuzzy_query_for_org_unit_by_name(db):
    """Should return a `match_phrase_prefix` query with the given arguments"""

    query = db.query_for_org_unit_by_name(
        name="Engineering", fuzzy_search=True
    )

    expected_index = "org_units"
    expected_query = {
        "size": 15,
        "_source": {"includes": ["uuid", "name", "addresses"]},
        "query": {"match_phrase_prefix": {"name": "Engineering"}},
    }

    expected = (expected_index, expected_query)

    assert query == expected


def test_query_for_org_unit_by_kle(db):
    """Should return a nested query with the given arguments"""

    index, query, processor = db.query_for_org_unit_by_kle(
        kle="Fest Udvalg", fuzzy_search=False
    )

    expected_index = "org_units"
    expected_query = {
        "size": 15,
        "_source": {"includes": ["uuid", "name"]},
        "query": {
            "nested": {
                "path": "kles",
                "inner_hits": {"_source": ["kles.title"]},
                "query": {
                    "match_phrase_prefix": {"kles.title": "Fest Udvalg"}
                },
            }
        },
    }

    assert index == expected_index
    assert query == expected_query
