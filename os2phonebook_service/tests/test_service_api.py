import pytest
from unittest import mock
from elasticsearch.exceptions import NotFoundError

from os2phonebook import __version__
from os2phonebook.app import initiate_application

from tests.fixtures.elasticsearch_data import (
    all_org_units_from_elasticsearch,
    one_unit_from_elasticsearch,
    one_employee_from_elasticsearch,
    no_matches_from_elasticsearch,
    one_employee_by_name_from_elasticsearch
)


# Settings
ORGANISATION_NAME = "Magenta Aps"


@pytest.fixture
def http_client():
    """Create the service (flask) app instance"""

    config = {
        "OS2PHONEBOOK_COMPANY_NAME": ORGANISATION_NAME,
        "OS2PHONEBOOK_STATIC_ROOT": "/static",
        "ELASTICSEARCH_HOST": "elasticsearch",
        "ELASTICSEARCH_PORT": 9600
    }

    app = initiate_application(config)
    return app.test_client()


def test_get_status_http_status(http_client):
    """Should return status code 200"""

    response = http_client.get("/api/status")
    assert response.status_code == 200


def test_get_status_metadata(http_client):
    """Should return the configured name and current version"""

    response = http_client.get("/api/status")

    json_response = response.get_json()

    expected = {
        "organisation": ORGANISATION_NAME,
        "version": __version__
    }

    assert json_response == expected


@mock.patch("os2phonebook.datastore.Elasticsearch.search", autospec=True)
def test_get_org_units_with_bad_results(mock_search, http_client):
    """Should return status code 500

    If the search for all organisation units yields no result,
    it most likely means the datastore has not yet been populated.
    As such the service should throw an error to signify that operations
    cannot be resumed.

    """

    mock_search.return_value = []

    response = http_client.get("/api/org_units")

    assert response.status_code == 500


@mock.patch("os2phonebook.datastore.Elasticsearch.search", autospec=True)
def test_get_org_units_with_good_results(mock_search, http_client):
    """Should return status code 200"""

    mock_search.return_value = all_org_units_from_elasticsearch()

    response = http_client.get("/api/org_units")

    assert response.status_code == 200


def test_org_unit_endpoint_no_uuid(http_client):
    """Unknow resources should cause a 404"""

    response = http_client.get("/api/org_unit")
    assert response.status_code == 404


@mock.patch("os2phonebook.datastore.Elasticsearch.get", autospec=True)
def test_get_org_unit_with_uuid(mock_get, http_client):
    """Should return status code 200"""

    mock_get.return_value = one_unit_from_elasticsearch()

    url = "/api/org_unit/1f06ed67-aa6e-4bbc-96d9-2f262b9202b5"
    response = http_client.get(url)
    assert response.status_code == 200


def test_get_employee_with_no_uuid(http_client):
    """Unknow resources should cause a 404"""

    response = http_client.get("/api/employee")
    assert response.status_code == 404


@mock.patch("os2phonebook.datastore.Elasticsearch.get", autospec=True)
def test_get_employee_with_uuid(mock_get, http_client):
    """Should return status code 200"""

    mock_get.return_value = one_employee_from_elasticsearch()

    url = "/api/employee/f16eee45-d96a-4efb-bd17-667d1795e13d"
    response = http_client.get(url)
    assert response.status_code == 200


@mock.patch("os2phonebook.datastore.Elasticsearch.get", autospec=True)
def test_get_employee_with_non_existing_identifier(mock_get, http_client):
    """Should return status code 404

    When calling the elasticsearch client get method
    with a target `_id` on a non-existing document,
    a NotFoundError will be raised.

    This should be propagated to a service error response of HTTP 404.

    """

    mock_get.side_effect = NotFoundError(404, "This _id does not exist")

    response = http_client.get("/api/employee/helllasdf")
    assert response.status_code == 404


def test_get_search(http_client):
    """Should return status code 202"""

    response = http_client.get("/api/search")
    assert response.status_code == 200


def test_get_search_schema(http_client):
    """Should return the search schema"""

    response = http_client.get("/api/search")

    json_response = response.get_json()

    expected_schema = {
        "format": "json",
        "method": "POST",
        "schema": {
            "search_type": {
                "required": True,
                "type": "string"
            },
            "search_value": {
                "required": True,
                "type": "string"
            }
        }
    }

    assert json_response == expected_schema


def test_post_search_with_no_body(http_client):
    """Should return status code 400"""

    response = http_client.post("/api/search")
    assert response.status_code == 400


def test_post_search_error_type_with_no_body(http_client):
    """Error message should display the InvalidRequestBody type"""

    response = http_client.post("/api/search")

    json_response = response.get_json()
    error_type = json_response["error"]["type"]

    expected_error_type = "InvalidRequestBody"
    assert error_type == expected_error_type


def test_post_search_error_type_with_incorrect_body(http_client):
    """Error message should display the InvalidRequestBody type"""

    post_payload = {
        "search_type": "employee_by_name"
    }

    response = http_client.post("/api/search", json=post_payload)
    json_response = response.get_json()

    error_type = json_response["error"]["type"]
    expected_error_type = "InvalidRequestBody"

    assert error_type == expected_error_type


@mock.patch("os2phonebook.datastore.Elasticsearch.search", autospec=True)
def test_post_search_with_no_results(mock_search, http_client):
    """Should return an empty list"""

    mock_search.return_value = no_matches_from_elasticsearch()

    post_payload = {
        "search_type": "employee_by_name",
        "search_value": "Picard"
    }

    response = http_client.post("/api/search", json=post_payload)

    results = response.get_json()

    expected_results = []

    assert results == expected_results


@mock.patch("os2phonebook.datastore.Elasticsearch.search", autospec=True)
def test_post_search_with_one_result(mock_search, http_client):
    """Should return an employee object (mock) with the given arguments"""

    mock_search.return_value = one_employee_by_name_from_elasticsearch()

    post_payload = {
        "search_type": "employee_by_name",
        "search_value": "Anne Yassen"
    }

    response = http_client.post("/api/search", json=post_payload)

    results = response.get_json()

    expected_results = [
        {
            "addresses": {
                "PHONE": [
                    {
                        "description": "Telefon",
                        "value": "61325558"
                    }
                ]
            },
            "name": "Anne Yassen",
            "uuid": "048c045c-02c4-45ab-a43f-bda6ac99448e"
        }
    ]

    assert results == expected_results