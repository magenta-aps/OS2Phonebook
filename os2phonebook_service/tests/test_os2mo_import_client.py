import pytest
from unittest import mock

from os2phonebook.integration import OS2MOImportClient

from tests.fixtures.os2mo_data import (
    organisation,
    org_unit_addresses,
    org_unit_engagements,
    org_unit_managers,
    org_unit_vacant_managers,
    org_unit_associations,
    single_employee,
    several_employees,
    employee_addresses,
    employee_engagements,
    employee_managers,
    employee_associations,
)


@pytest.fixture
def os2mo_client():
    """Reusable OS2MOImportClient fixture

    Returns:
        `:obj:OS2MOImportClient`: An instance of the OS2MOImportClient

    """

    fake_url = "https://os2mo.testing.org"
    client = OS2MOImportClient(fake_url)

    # Two built in methods are requiring the org uuid
    # If this is not set, an actual HTTP request must be made
    #
    # if not self.organisation_uuid:
    #        self.update_org_uuid()
    #
    # By pre-setting the value, mocking for the update method can be avoided
    client.organisation_uuid = "aed38686-ac20-40e0-9053-958c817ed042"

    return client


def test_configure_access_token(os2mo_client):
    """Should set the `SESSIONS` header on the session instance"""

    fake_token = "SECRETTOKENVALUE"
    os2mo_client.configure_access_token(fake_token)

    session_header = os2mo_client.session.headers["SESSION"]

    assert session_header == fake_token


@mock.patch("os2phonebook.integration.OS2MOImportClient.get")
def test_update_org_uuid(mock_request, os2mo_client):
    """Should extract an set the organisation uuid"""

    mock_request.return_value = organisation()

    expected = "3b866d97-0b1f-48e0-8078-686d96f430b3"

    os2mo_client.update_org_uuid()

    assert os2mo_client.organisation_uuid == expected


@mock.patch("os2phonebook.integration.OS2MOImportClient.get", autospec=True)
def test_get_org_unit_address_references(mock_request, os2mo_client):
    """Should return the converted and categorized address references"""

    mock_request.return_value = org_unit_addresses()

    expected = {
        "DAR": [
            {
                "description": "Returadresse",
                "value": "Castenskjoldsvej 2, 2., 6000 Kolding",
            },
            {
                "description": "Henvendelsessted",
                "value": "Castenskjoldsvej 2, 2., 6000 Kolding",
            },
            {
                "description": "Postadresse",
                "value": "Castenskjoldsvej 2, 2., 6000 Kolding",
            },
        ],
        "PHONE": [],
        "EMAIL": [{"description": "Email", "value": "info@kolding.dk"}],
        "EAN": [{"description": "EAN-nummer", "value": "1224321145484"}],
        "PNUMBER": [{"description": "P-nummer", "value": "1866728518"}],
        "WWW": [{"description": "Webadresse", "value": "www.kolding.dk"}],
    }

    method_result = os2mo_client.get_org_unit_address_references(
        uuid="3b866d97-0b1f-48e0-8078-686d96f430b3"
    )

    assert method_result == expected


@mock.patch("os2phonebook.integration.OS2MOImportClient.get", autospec=True)
def test_get_org_unit_engagement_references(mock_request, os2mo_client):
    """Should return the converted/trimmed engagement references"""

    # Moch request return data
    mock_request.return_value = org_unit_engagements()

    expected = [
        {
            "name": "Lykke Skytte Hansen",
            "title": "Specialkonsulent",
            "uuid": "eff3fca2-645c-4613-90ad-5fb47db47bc7",
        },
        {
            "name": "Johannes Engmann Korsgård Maaløe",
            "title": "Ressourcepædagog",
            "uuid": "be39de52-060a-4ae3-b705-ba46dd9b27a6",
        },
        {
            "name": "Christian Fregerslev Ulriksen",
            "title": "Teknisk Servicemedarb.",
            "uuid": "6037238b-a013-4520-86c8-b2ea15ee88d5",
        },
    ]

    method_result = os2mo_client.get_org_unit_engagement_references(
        uuid="3b866d97-0b1f-48e0-8078-686d96f430b3"
    )

    assert method_result == expected


@mock.patch("os2phonebook.integration.OS2MOImportClient.get", autospec=True)
def test_get_org_unit_manager_references(mock_request, os2mo_client):
    """Should return converted manager references"""

    # Mock request return data
    mock_request.return_value = org_unit_managers()

    expected = [
        {
            "name": "Peter Behrens Høgfeldt",
            "title": "Direktør",
            "uuid": "84f4536f-52d4-4229-a675-9a92d71be79c",
        }
    ]

    method_result = os2mo_client.get_org_unit_manager_references(
        uuid="3b866d97-0b1f-48e0-8078-686d96f430b3"
    )

    assert method_result == expected


@mock.patch("os2phonebook.integration.OS2MOImportClient.get", autospec=True)
def test_get_org_unit_vacant_managers(mock_request, os2mo_client):
    """Should not return manager references if no `person` is defined"""

    # Moch request return data
    mock_request.return_value = org_unit_vacant_managers()

    expected = []

    method_result = os2mo_client.get_org_unit_manager_references(
        uuid="3b866d97-0b1f-48e0-8078-686d96f430b3"
    )

    assert method_result == expected


@mock.patch("os2phonebook.integration.OS2MOImportClient.get", autospec=True)
def test_get_org_unit_association_references(mock_request, os2mo_client):
    """Should return converted association reference(s)"""

    # Moch request return data
    mock_request.return_value = org_unit_associations()

    expected = [
        {
            "name": "Hans Pie Rasmussen",
            "title": "Næstformand",
            "uuid": "1acb3999-423a-48c4-9ef8-ba4452929d7a",
        }
    ]

    method_result = os2mo_client.get_org_unit_association_references(
        uuid="3b866d97-0b1f-48e0-8078-686d96f430b3"
    )

    assert method_result == expected


@mock.patch("os2phonebook.integration.OS2MOImportClient.get", autospec=True)
def test_get_total_employees(mock_request, os2mo_client):
    """Should extract the total value from the request"""

    mock_request.return_value = single_employee()

    expected = 897

    method_result = os2mo_client.get_total_employees()

    assert method_result == expected


@mock.patch("os2phonebook.integration.OS2MOImportClient.get", autospec=True)
def test_get_batch_of_employees(mock_request, os2mo_client):
    """Should return a batch of employees"""

    mock_request.return_value = several_employees()

    expected = [
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
    ]

    method_result = os2mo_client.get_batch_of_employees(offset=0, batch_size=4)

    assert method_result == expected


@mock.patch("os2phonebook.integration.OS2MOImportClient.get", autospec=True)
def test_get_employee_address_references(mock_request, os2mo_client):
    """Should return converted address references"""

    mock_request.return_value = employee_addresses()

    expected = {
        "DAR": [
            {
                "description": "Postadresse",
                "value": "Frederiksgade 11E, 5700 Svendborg",
            }
        ],
        "EAN": [],
        "EMAIL": [{"description": "Email", "value": "annb@svendborg.dk"}],
        "PHONE": [],
        "PNUMBER": [],
        "WWW": [],
    }

    method_result = os2mo_client.get_employee_address_references(
        uuid="3b866d97-0b1f-48e0-8078-686d96f430b3"
    )

    assert method_result == expected


@mock.patch(
    "os2phonebook.integration.OS2MOImportClient.get_org_unit", autospec=True
)
@mock.patch("os2phonebook.integration.OS2MOImportClient.get", autospec=True)
def test_get_employee_engagement_references(
    mock_request, mock_org_unit, os2mo_client
):
    """Should return converted engagement references"""

    mock_request.return_value = employee_engagements()

    expected = [
        {
            "name": "Svendborg Kommune",
            "title": "Timelønnet lærer",
            "uuid": "f06ee470-9f17-566f-acbe-e938112d46d9",
        }
    ]

    method_result = os2mo_client.get_employee_engagement_references(
        uuid="3b866d97-0b1f-48e0-8078-686d96f430b3"
    )

    assert method_result == expected


@mock.patch(
    "os2phonebook.integration.OS2MOImportClient.get_org_unit", autospec=True
)
@mock.patch("os2phonebook.integration.OS2MOImportClient.get", autospec=True)
def test_get_employee_manager_references(
    mock_request, mock_org_unit, os2mo_client
):
    """Should return converted manager references"""

    mock_request.return_value = employee_managers()

    expected = [
        {
            "name": "Direktør område Anne Vang",
            "title": "Direktør",
            "uuid": "d9ccd8f8-7c7c-4788-80c0-cfc3dd7ff6ce",
        }
    ]

    method_result = os2mo_client.get_employee_manager_references(
        uuid="3b866d97-0b1f-48e0-8078-686d96f430b3"
    )

    assert method_result == expected


@mock.patch(
    "os2phonebook.integration.OS2MOImportClient.get_org_unit", autospec=True
)
@mock.patch("os2phonebook.integration.OS2MOImportClient.get", autospec=True)
def test_get_employee_association_references(
    mock_request, mock_org_unit, os2mo_client
):
    """Should return converted association references"""

    mock_request.return_value = employee_associations()

    expected = [
        {
            "name": "Byg",
            "title": "Ansat",
            "uuid": "6e95168a-82a5-40a7-b533-8a771c2f1fbb",
        },
        {
            "name": "L-MED Center for By Erhverv og Miljø",
            "title": "Medlem",
            "uuid": "25448337-42e4-459f-8bdf-0e3da90a58f0",
        },
    ]

    method_result = os2mo_client.get_employee_association_references(
        uuid="3b866d97-0b1f-48e0-8078-686d96f430b3"
    )

    assert method_result == expected
