from typing import List, Tuple
from urllib.parse import urljoin
from requests import Session, RequestException
from os2phonebook.helpers import log_factory


# Init loggign
log = log_factory()


class OS2MOImportClient:
    """Client for importing org units and employees from the OS2MO service api.

    This client uses requests.Session for HTTP(s) communication.

    Attributes:
        base_url (str): OS2MO service url, e.g. https://os2mo.magenta.dk
        session (str): An instance of requests.Session
        organisation_uuid (str): Main organisation identifier <uuid>
        org_unit_map (dict): Hashmap for temporarily storing org units
        employee_map (dict): Hashmap for temporarily storing employees

    """

    def __init__(self, base_url: str, session: Session = Session):
        self.base_url = base_url
        self.session = session()
        self.organisation_uuid = ""
        self.org_unit_map = {}
        self.employee_map = {}

    def configure_access_token(self, token: str):
        """Optionally configure the http client with an auth session header."""

        os2mo_session = {
            "SESSION": token
        }

        self.session.headers.update(os2mo_session)

    def get(self, resource: str, **query_params) -> dict:
        """HTTP GET convenience wrapper

        For the lazy folks who enjoy not having
        to type out the full URL for each api call.

        Args:
            resource (str): HTTP resource path relative to the service api.
                Example: resource = `service/o`
                converts to https://os2mo.magnenta.dk/service/o/

            **query_params (kwargs): Arbitrary key value pairs
                which are passed on as query params to the underlying method

        Raises:
            RequestException: If the service api returns a negative status code.

        Returns:
            dict: JSON response body as a dictionary

        """

        resource_url = urljoin(self.base_url, resource)

        response = self.session.get(url=resource_url, params=query_params)

        if not response.ok:
            log.debug(response)
            raise RequestException(f"HTTP_OS2MO_RESPONSE_ERROR: {response.status_code}")

        return response.json()

    def update_org_uuid(self):
        """Retrieve the identifier of the main organisation and update the attribute.

        The service endpoint `https//os2mo.magenta.dk/service/o/' returns
        a list of organisations.

        Currently there should be only be support for 1 organisation,
        hence we're assuming that the first result will be the main organisation.

        Raises:
            AttributeError: If the response does not contain at least one
            organisation in the json payload.

        Example:
            The response body should contain a structure as follows:

            [
                {
                    "name": "Kolding Kommune",
                    "user_key": "Kolding Kommune",
                    "uuid": "3b866d97-0b1f-48e0-8078-686d96f430b3"
                }
            ]


        """
        # Proceed to retrieve the organisation uuid
        resource = "service/o/"

        return_data = self.get(resource)

        # Assuming that the main organisation is the first one in the list
        # Does this not sound quite resonable ?
        organisation_uuid = return_data[0]["uuid"]

        if not organisation_uuid:
            raise AttributeError("MAIN_ORG_ATTRIBUTE_DOES_NOT_EXIST_ERROR")

        self.organisation_uuid = organisation_uuid

    def address_adapter(self, address_data: list) -> dict:
        """OS2MO address type adapter

        Converts OS2MO address details into a simple object:

        {
            "description": "Postadresse",
            "value": "Kildeparken 64A, Seest, 6000 Kolding"
        }

        And aggregates all address objects into lists of the following categories:
            * DAR (Residence addresses)
            * PHONE (Phone numbers)
            * EMAIL (Email addresses)
            * EAN (European Article Numbering)
            * WWW (Web address)

        Args:
            address_data (list): A list of OS2MO response data objects <dict>

        Returns:
            dict: Address types map containing a list for each type of addresses

        Example:

            "addresses": {
                "DAR": [
                    {
                        "description": "Postadresse",
                        "value": "Kildeparken 64A, Seest, 6000 Kolding"
                    }
                ],
                "EAN": [
                    {
                        "description": "EAN-nummer",
                        "value": "2617445301464"
                    }
                ],
                "EMAIL": [
                    {
                        "description": "Email",
                        "value": "Budget_og_Planlægning@kolding.dk"
                    }
                ],
                "PHONE": [],
                "PNUMBER": [
                    {
                        "description": "P-nummer",
                        "value": "5424825851"
                    }
                ],
                "WWW": []
                },
                "associations": [
                    {
                        "name": "Mathilde Olsen",
                        "title": "Medarbejder",
                        "uuid": "7faf0a01-85ff-42eb-9b21-0101b1de5685"
                    }
                ],
                "engagements": [
                {
                    "name": "Qais Udstad Gade",
                    "title": "Lærer/Overlærer",
                    "uuid": "8441b33b-ca64-403d-93d3-44357a05c669"
                }
            }

        """
        address_types = {
            "DAR": [],
            "PHONE": [],
            "EMAIL": [],
            "EAN": [],
            "PNUMBER": [],
            "WWW": []
        }

        for address in address_data:

            scope = address["address_type"]["scope"]

            if scope not in address_types:
                log.debug(f"Scope: {scope} does not exist")
                continue

            if "visibility" in address and address["visibility"]["scope"] == "SECRET":
                continue

            formatted_address = {
                "description": address["address_type"]["name"],
                "value": address["name"]
            }

            address_types[scope].append(formatted_address)

        return address_types

    def get_org_unit(self, uuid: str) -> None:
        """Retrieve and convert org unit

        The converted unit will be temporarily stored
        in the `employee_map` hashmap attribute.

        Example (converted org unit):

        {
            "org_unit": {
                "name": "Budget og Planlægning",
                "parent": "b6c11152-0645-4712-a207-ba2c53b391ab",
                "uuid": "1f06ed67-aa6e-4bbc-96d9-2f262b9202b5"
                "addresses": {
                    "DAR": [],
                    "EAN": [],
                    "EMAIL": [],
                    "PHONE": [],
                    "PNUMBER": [
                        {
                            "description": "P-nummer",
                            "value": "5424825851"
                        }
                    ],
                    "WWW": []
                    },
                    "associations": [
                        {
                            "name": "Mathilde Olsen",
                            "title": "Medarbejder",
                            "uuid": "7faf0a01-85ff-42eb-9b21-0101b1de5685"
                        }
                    ],
                    "engagements": [
                        {
                            "name": "Qais Udstad Gade",
                            "title": "Lærer/Overlærer",
                            "uuid": "8441b33b-ca64-403d-93d3-44357a05c669"
                        }
                    ],
                    "management": [
                        {
                            "name": "Jan Elkjær Winther Nielsen",
                            "title": "Direktør",
                            "uuid": "f16eee45-d96a-4efb-bd17-667d1795e13d"
                        }
                    ]
                }
            }
        }

        Args:
            uuid (str): Document identifier.

        """

        resource = f"service/ou/{uuid}"

        if uuid in self.org_unit_map:
            return

        return_data = self.get(resource)

        unit = {
            "uuid": return_data["uuid"],
            "name": return_data["name"]
        }

        # Enrich unit (It's just a nicer way to say mutate)
        unit["addresses"] = self.get_org_unit_address_references(uuid)
        unit["engagements"] = self.get_org_unit_engagement_references(uuid)
        unit["associations"] = self.get_org_unit_association_references(uuid)
        unit["management"] = self.get_org_unit_manager_references(uuid)

        parent = return_data["parent"]

        if parent:
            parent_uuid = parent["uuid"]
            unit["parent"] = parent_uuid

            self.get_org_unit(parent_uuid)

        else:
            unit["parent"] = None

        self.org_unit_map[uuid] = unit

    def get_org_unit_address_references(self, uuid: str):
        """Retrieve and convert org unit addresses os2mo.

        Once the addresses are retrieve,
        they are passed on to the `address_adapter` method.

        Args:
            uuid (str): Document identifier

        """

        # Define scopes to import
        # Potentially there could be a number of additional
        # scopes within the instance of the OS2MO webapi.
        # However we are only interested in displaying the scopes
        # hardcoded in the list below.

        resource = f"service/ou/{uuid}/details/address"
        return_data = self.get(resource)

        return self.address_adapter(return_data)

    def get_org_unit_engagement_references(self, uuid) -> List[dict]:
        """Retrieve and convert engagement data

        Converts engagement details object to a list of job function titles
        with references / uuid to the org unit.

        Args:
            uuid (str): Document identifier

        Returns:
            List[dict]: A list of reference objects.

        Example:
            [
                {
                    "name": "Qais Udstad Gade",
                    "title": "Lærer/Overlærer",
                    "uuid": "8441b33b-ca64-403d-93d3-44357a05c669"
                }
            ]

        """
        resource = f"service/ou/{uuid}/details/engagement"
        return_data = self.get(resource)

        return [
            {
                "title": data["job_function"]["name"],
                "name": data["person"]["name"],
                "uuid": data["person"]["uuid"],
            }
            for data in return_data
        ]

    def get_org_unit_manager_references(self, uuid: str):
        """Retrieve and convert manager data

        Converts a manager object to a list of manager titles
        and reference uuids.

        Args:
            uuid (str): Document identifier

        Returns:
            List[dict]: A list of reference objects.

        Example:
            [
                {
                    "name": "Jan Elkjær Winther Nielsen",
                    "title": "Direktør",
                    "uuid": "f16eee45-d96a-4efb-bd17-667d1795e13d"
                }
            ]

        """

        resource = f"service/ou/{uuid}/details/manager"
        return_data = self.get(resource)

        managers = []

        for data in return_data:

            # A manager position can be vacant
            # This means there may be no person associated with it
            if not data["person"]:
                continue

            manager = {
                "title": data["manager_type"]["name"],
                "name": data["person"]["name"],
                "uuid": data["person"]["uuid"],
            }

            managers.append(manager)

        return managers

    def get_org_unit_association_references(self, uuid):
        """Retrieve and convert association data

        Converts a manager object to a list of association titles
        and reference uuids.

        Args:
            uuid (str): Document identifier

        Returns:
            List[dict]: A list of reference objects.

        Example:
            [
                {
                    "name": "Mathilde Olsen",
                    "title": "Medarbejder",
                    "uuid": "7faf0a01-85ff-42eb-9b21-0101b1de5685"
                }
            ]

        """
        resource = f"service/ou/{uuid}/details/association"
        return_data = self.get(resource)

        return [
            {
                "title": data["association_type"]["name"],
                "name": data["person"]["name"],
                "uuid": data["person"]["uuid"],
            }
            for data in return_data
        ]

    def get_total_employees(self) -> int:
        """Retrieve the total amount of employees of the main organisation

        Returns:
            int: Total amount of employees

        """

        if not self.organisation_uuid:
            self.update_org_uuid()

        resource = f"service/o/{self.organisation_uuid}/e"

        return_data = self.get(resource, limit=1)

        total = return_data["total"]

        return int(total)

    def get_batch_of_employees(self, offset=0, batch_size=1) -> List[dict]:
        """Retrieve a configurable batch of employees.

        By fetching a smaller batch, pagination logic can be skipped.

        Args:
            offset (int): Result index offset
            batch_size (int): Result batch size
                e.g. batch=10 means 10 employees returned

        Returns:
            List[dict]: List of unmodified employees from OS2MO

        Example:

            [
                {
                "givenname": "Aage Bruun Lund",
                "name": "Aage Bruun Lund Happe",
                "surname": "Happe",
                "uuid": "26d43382-ce39-4772-aee5-c711732ca345"
                },
            ]

        """

        if not self.organisation_uuid:
            self.update_org_uuid()

        resource = f"service/o/{self.organisation_uuid}/e"

        return_data = self.get(resource, start=offset, limit=batch_size)

        return [
            employee
            for employee in return_data["items"]
        ]

    def get_employee_address_references(self, uuid):
        """Retrieve and convert employee addresses.

        Once the addresses are retrieve,
        they are passed on to the `address_adapter` method.

        Args:
            uuid (str): Document identifier

        """
        resource = f"service/e/{uuid}/details/address"
        return_data = self.get(resource)

        return self.address_adapter(address_data=return_data)

    def get_employee_engagement_references(self, uuid) -> List[dict]:
        """Retrieve and convert employee engagements.

        Converts a engagements object to a list of titles
        and references to the attached org unit.

        Args:
            uuid (str): Document identifier

        Returns:
            List[dict]: A list of reference objects.

        Example:

            [
                {
                    "name": "Kolding Kommune",
                    "title": "Kontorelev",
                    "uuid": "f06ee470-9f17-566f-acbe-e938112d46d9"
                }
            ]

        """
        resource = f"service/e/{uuid}/details/engagement"
        return_data = self.get(resource)

        for data in return_data:
            org_unit_uuid = data["org_unit"]["uuid"]
            self.get_org_unit(org_unit_uuid)

        return [
            {
                "title": data["job_function"]["name"],
                "name": data["org_unit"]["name"],
                "uuid": data["org_unit"]["uuid"],
            }
            for data in return_data
        ]

    def get_employee_manager_references(self, uuid) -> List[dict]:
        """Retrieve and convert employee manager titles

        Converts a manager object to a list of manager titles
        and reference uuids.

        Args:
            uuid (str): Document identifier

        Returns:
            List[dict]: A list of reference objects.

        Example:

            [
                {
                    "name": "Kolding Kommune",
                    "title": "Direktør",
                    "uuid": "f06ee470-9f17-566f-acbe-e938112d46d9"
                }
            ]
        """

        resource = f"service/e/{uuid}/details/manager"
        return_data = self.get(resource)

        for data in return_data:
            org_unit_uuid = data["org_unit"]["uuid"]
            self.get_org_unit(org_unit_uuid)

        return [
            {
                "title": data["manager_type"]["name"],
                "name": data["org_unit"]["name"],
                "uuid": data["org_unit"]["uuid"],
            }
            for data in return_data
        ]

    def get_employee_association_references(self, uuid) -> List[dict]:
        """Retrieve and convert employee associations

        Converts a manager object to a list of association titles
        and reference uuids.

        Args:
            uuid (str): Document identifier

        Returns:
            List[dict]: A list of reference objects.

        Example:
            [
               {
                    "name": "Budget og Planlægning",
                    "title": "Medarbejder",
                    "uuid": "1f06ed67-aa6e-4bbc-96d9-2f262b9202b5"
                }
            ]

        """

        resource = f"service/e/{uuid}/details/association"
        return_data = self.get(resource)

        for data in return_data:
            org_unit_uuid = data["org_unit"]["uuid"]
            self.get_org_unit(org_unit_uuid)

        return [
            {
                "title": data["association_type"]["name"],
                "name": data["org_unit"]["name"],
                "uuid": data["org_unit"]["uuid"],
            }
            for data in return_data
        ]

    def import_routine(self) -> Tuple[dict, dict]:
        """Import all employees and associated org units from OS2MO.
        
        Higher level import routine which imports all employees
        in batches and recusively imports the associated org units.

        TODO:
            * Make it prettier and perhaps testable.

        Note:
            This method has more verbose logging for debugging purposes.
            The import log should be a seperate log file
            as to not polute the service log. 

            (This is handled automatically by the bootstrapper)

        Returns:
            Tuple[dict, dict]: A tuple containing a dicts
                of employees and org unit hashmaps

        """
        total = self.get_total_employees()
        log.info(f"OS2MO_IMPORT_ROUTINE - Total employees to import {total}")

        # Start offset
        offset = 0

        # Get batches of 250 employees
        batch_size = 250

        while total >= offset:

            # Silly math for logging purposes
            current_batch_end = offset + batch_size
            if current_batch_end > total:
                current_batch_end = total

            log.info(f"OS2MO_IMPORT_ROUTINE - Import batch {offset}-{current_batch_end}")

            employees = self.get_batch_of_employees(
                offset=offset,
                batch_size=batch_size
            )

            for employee in employees:
                # We'll need this in a bit
                uuid = employee["uuid"]

                # Enrich employee         
                employee["engagements"] = self.get_employee_engagement_references(uuid)
                employee["associations"] = self.get_employee_association_references(uuid)
                employee["management"] = self.get_employee_manager_references(uuid)

                # Do NOT import employees without an engagement or association
                # https://redmine.magenta-aps.dk/issues/34812

                # We do however want to import employees with management roles.
                # As an external employee may be a manager for an organisation unit.

                if not employee["associations"] and not employee["engagements"] and not employee["management"]:
                    log.info(
                        "OS2MO_IMPORT_ROUTINE Skip employee due to missing engagements, associations, management"
                    )

                    # Reference to the skipped employee to debug log
                    log.debug(
                        f"OS2MO_IMPORT_ROUTINE - NO_RELATIONS_TO_ORG_UNIT employee={uuid}"
                    )

                    continue

                employee["addresses"] = self.get_employee_address_references(uuid)

                self.employee_map[uuid] = employee

            log.info(f"OS2MO_IMPORT_ROUTINE - Batch {current_batch_end}-{current_batch_end} completed")
            
            # Hacky offset update
            offset = offset + batch_size

        return (self.employee_map, self.org_unit_map)
