from typing import List, Tuple
from elasticsearch import Elasticsearch
from os2phonebook.exceptions import InvalidSearchType


def create_connection(host: str, port: int) -> Elasticsearch:
    """Elasticsearch connection factory.

    This is a connection factory to connect to the
    Elasticsearch backend

    Args:
        host (str): Hostname of the backend
        port (int): Service port

    Returns:
        :obj:`Elasticsearch`: An instance of the elasticsearch client

    """
    if not isinstance(host, str):
        raise TypeError("Host description must be passed as a string")

    if not isinstance(port, int):
        raise TypeError("Port identifier must be passed as an integer")

    db = Elasticsearch([
        {
            'host': host,
            'port': port
        },
    ])

    return db


class DataStore(object):
    """Client for generating queries in backend datastore

    Args:
        db (:obj:`Elasticsearch`): Instance of the elasticsearch client

    """

    def __init__(self, db):

        if not isinstance(db, Elasticsearch):
            raise TypeError("Datastore requires an instance of the Elasticsearch object")

        self.db = db

    def get_employee(self, uuid: str) -> dict:
        """Retrieve employee document by identifer

        Args:
            uuid (str): Document identifier <uuid>

        Returns:
            dict: Document containing employee

        """

        index = "employees"
        response = self.db.get(index=index, id=uuid)

        # _source contains the actual document
        employee = response["_source"]

        return employee

    def get_org_unit(self, uuid: str) -> dict:
        """Retrieve org_unit document by identifer

        Args:
            uuid (str): Document identifier <uuid>

        Returns:
            dict: Document containing org_unit

        """

        index = "org_units"
        response = self.db.get(index=index, id=uuid)

        # _source contains the actual document
        org_unit = response["_source"]

        return org_unit

    def get_size(self, index: str) -> int:
        """Get the total document count for a given index

        Args:
            index (str): Name of the index to query

        Returns:
            int: Total documents value

        """

        query = {
            "size": 0,
            "query": {
                "match_all": {}
            }
        }

        response_data = self.db.search(index=index, body=query)
        total_size = response_data["hits"]["total"]["value"]

        return int(total_size)

    def get_all_org_units(self) -> List[dict]:
        """Retrieve all org unit documents from the store

        Returns:
            List[dict]: An array of org unit documents as dictionaries

        """

        index = "org_units"

        # Calculate total document size
        total_size = self.get_size(index)

        # Scoped query
        # Documents returned only contains values for
        # * uuid
        # * org unit name
        # * parent unit uuid
        query = {
            "size": total_size,
            "query": {
                "match_all": {}
            },
            "_source": {
                "includes": [
                    "uuid",
                    "name",
                    "parent",
                ]
            }
        }

        return_data = self.db.search(index=index, body=query)

        hits = return_data["hits"]["hits"]

        return [
            unit["_source"]
            for unit in hits if "_source" in unit
        ]

    def search(self, search_type, search_value, fuzzy_search=False) -> List[dict]:
        """High level search method

        Generates search query based on the search type by
        calling the underlying query method.

        Available search types:
            * employee_by_name
            * employee_by_phone
            * employee_by_email
            * employee_by_engagement
            * org_unit_by_name

        Args:
            search_type (str): Search type (see available types above)
            search_value (str): Arbitrary search string
            fuzzy_search (bool): If True, use match_phrase_prefix

        Returns:
            List[dict]: A list of documents that matched the search

        Example:

            results = client.search(
                search_type = "employee_by_name",
                search_value = "Commander Riker",
                fuzzy_search = True
            )

        """

        if search_type == "employee_by_name":
            index, query = self.query_for_employee_by_name(search_value, fuzzy_search)

        elif search_type == "employee_by_phone":
            index, query = self.query_for_employee_by_phone(search_value, fuzzy_search)

        elif search_type == "employee_by_email":
            index, query = self.query_for_employee_by_email(search_value, fuzzy_search)

        elif search_type == "employee_by_engagement":
            index, query = self.query_for_employee_by_engagement(search_value, fuzzy_search)

        elif search_type == "org_unit_by_name":
            index, query = self.query_for_org_unit_by_name(search_value, fuzzy_search)

        else:
            raise InvalidSearchType(f"Search type: {search_type} is not available")

        print(query)

        response = self.db.search(index=index, body=query)

        return [
            document["_source"]
            for document in response["hits"]["hits"]
        ]

    def _query_match(self, search_field: str, search_value: str, size: int, source_filter: list) -> dict:
        """Generate a query to match full names/keywords.

        Consider the following search:
            search_value = "ba"

        Searching by prefix would yield the following results:
            * banana
            * batman
            * Ali baba
            * The little bakery

        This type of query will only return results will a full match on keywords
        and is typically used as the initial search before attempting to broader searches.

        For example:
            search_type = "cake" will return only "cake" and not "beefcake"

        Args:
            search_field (str): Name of the document field to search in.
            search_value (str): Arbitrary search string
            size (int): Amount of documents to return
            source_filter (list): List of field names to return

        Returns:
            dict: Elastic search query

        """

        query = {
            "size": size,
            "_source": {
                "includes": list(source_filter)
            },
            "query": {
                "match": {
                    search_field: search_value
                }
            }
        }

        return query

    def _query_match_phrase_prefix(self, search_field: str, search_value: str, size: int, source_filter: list) -> dict:
        """Generate a query to match on the search prefix.

        Unlike `match query` this is a broader search query,
        matching on everything that `starts with`.

        This is typically used as a second search attempt if there was no initial match.

        For example:
            search_type = "ho" will return only "holiday" but not "shoo"

        Args:
            search_field (str): Name of the document field to search in.
            search_value (str): Arbitrary search string
            size (int): Amount of documents to return

            *args (args): List of field names to return

        Returns:
            dict: Elastic search query

        """

        query = {
            "size": int(size),
            "_source": {
                "includes": list(source_filter)
            },
            "query": {
                "match_phrase_prefix": {
                    search_field: search_value
                }
            }
        }

        return query

    def query_for_employee_by_name(self, name: str, fuzzy_search: bool) -> Tuple[str, dict]:
        """Search query for an employee by his or her name.

        Args:
            name (str): Name of the document field to search in.
            fuzzy_search (bool): Search wider if True

        Returns:
            Tuple[str, dict]: Index name (str) and Elastic search query (dict)

        """

        index = "employees"

        source_filter = [
            "uuid",
            "name",
            "addresses.PHONE",
        ]

        if fuzzy_search:
            search_field = "givenname"
            query = self._query_match_phrase_prefix(search_field, name, 15, source_filter)
        else:
            query = {
                "_source": {
                    "includes": list(source_filter)
                },
                "query": {
                    "multi_match": {
                        "query": str(name),
                        "type": "cross_fields",
                        "fields": ["surname", "givenname"],
                        "tie_breaker": 0.3
                    }
                }
            }

        return (index, query)

    def query_for_employee_by_phone(self, phone_number: str, fuzzy_search: bool) -> Tuple[str, dict]:
        """Search query for an employee by phone number.

        Args:
            phone_number (str): Phone number, e.g. 21223344.
            fuzzy_search (bool): Search wider if True.

        Returns:
            Tuple[str, dict]: Index name (str) and Elastic search query (dict)

        """

        index = "employees"
        search_field = "addresses.PHONE.value"

        source_filter = [
            "uuid",
            "name",
            "addresses.PHONE"
        ]

        if fuzzy_search:
            query = self._query_match_phrase_prefix(search_field, phone_number, 15, source_filter)
        else:
            query = self._query_match(
                search_field, phone_number, 15, *source_filter
            )

        return (index, query)

    def query_for_employee_by_email(self, email_address: str, fuzzy_search: bool) -> Tuple[str, dict]:
        """Search query for an employee by email address.

        Args:
            email_address (str): Email address, e.g. mail@example.com.
            fuzzy_search (bool): Search wider if True.

        Returns:
            Tuple[str, dict]: Index name (str) and Elastic search query (dict)

        """

        index = "employees"
        search_field = "addresses.EMAIL.value"

        source_filter = [
            "uuid",
            "name",
            "addresses.EMAIL"
        ]

        query = self._query_match_phrase_prefix(search_field, email_address, 15, source_filter)
        return (index, query)

    def query_for_org_unit_by_name(self, name: str, fuzzy_search: bool):
        """Search query for an org unit by name.

        Args:
            name (str): Name of the org unit, e.g. `Command bridge`
            fuzzy_search (bool): Search wider if True.

        Returns:
            Tuple[str, dict]: Index name (str) and Elastic search query (dict)

        """

        index = "org_units"
        search_field = "name"

        source_filter = [
            "uuid",
            "name",
            "addresses"
        ]

        query = self._query_match_phrase_prefix(search_field, name, 15, source_filter)
        return (index, query)

    def delete_index(self, index: str) -> dict:
        """Delete an entire index by name

        Args:
            index (str): Name of the index

        Returns:
            dict: Elasticsearch json response as dictionary

        """

        response = self.db.indices.delete(index=index, ignore=[400, 404])

        return response

    def insert_index(self, index: str, identifier: str, data: dict) -> dict:
        """Insert a document into a datastore index

        Args:
            index (str): Name of the index
            identifier (str): Create identifier for the document
            data (dict): Document as a dictionary

        Returns:
            dict: Elasticsearch json response as dictionary

        """

        response = self.db.index(
            index=index, doc_type="_doc", id=identifier, body=data
        )

        return response
