from typing import List, Tuple, Callable
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
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

    db = Elasticsearch([{"host": host, "port": port}])

    return db


class DataStore(object):
    """Client for generating queries in backend datastore

    Args:
        db (:obj:`Elasticsearch`): Instance of the elasticsearch client.

        search_type_map (dict): A map of all the available search types.

            Available search types:
                * employee_by_name
                * employee_by_phone
                * employee_by_email
                * employee_by_engagement
                * org_unit_by_name
                * org_unit_by_kle

            Example:

            {
                "employee_by_name": {
                    "description": "Navn",
                    "query_method": "query_for_employee_by_name"
            }

            This particular search type has the canonical description `Navn`
            and a query method which refers to the name of an attribute
            on this class, e.g. `Datastore.query_for_employee_by_name`.

    """

    def __init__(self, db):

        if not isinstance(db, Elasticsearch):
            raise TypeError(
                "Datastore requires an instance of the Elasticsearch object"
            )

        self.db = db

        self.search_type_map = {
            "employee_by_name": {
                "description": "Navn",
                "query_method": "query_for_employee_by_name",
            },
            "employee_by_phone": {
                "description": "Telefon",
                "query_method": "query_for_employee_by_phone",
            },
            "employee_by_email": {
                "description": "Email",
                "query_method": "query_for_employee_by_email",
            },
            "employee_by_engagement": {
                "description": "Stilling",
                "query_method": "query_for_employee_by_engagement",
            },
            "org_unit_by_name": {
                "description": "Enhed",
                "query_method": "query_for_org_unit_by_name",
            },
            "org_unit_by_kle": {
                "description": "Enhed",
                "query_method": "query_for_org_unit_by_kle",
            },
        }

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

        query = {"size": 0, "query": {"match_all": {}}}

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
            "query": {"match_all": {}},
            "_source": {"includes": ["uuid", "name", "parent"]},
        }

        return_data = self.db.search(index=index, body=query)

        hits = return_data["hits"]["hits"]

        return [unit["_source"] for unit in hits if "_source" in unit]

    def get_query_method(
        self, search_type: str
    ) -> Callable[[str, bool], Tuple[str, dict]]:
        """Fetches query generator based on the `search_type`

        Please see the `search_type_map` attribute
        for more information on the available types.

        Args:
            search_type (str): This refers to the `search_type_map` key.

        Returns:
            Callable[[str, bool], Tuple[str, dict]: The query generator

        Raises:
            TypeError:
                If the `search_type` is not a string value.
            InvalidSearchType:
                If the `search_type` does not exist.
                (Meaning that it does not exist in the `search_type_map`)
            ValueError:
                If the query method is not defined for this type.
            AttributeError:
                If the query method defined does not exist as an attribute.
        """

        if not isinstance(search_type, str):
            raise TypeError("Search type must be a string value")

        if search_type not in self.search_type_map:
            raise InvalidSearchType(
                f"Search type: {search_type} is not available"
            )

        selected_type = self.search_type_map[search_type]

        if "query_method" not in selected_type:
            raise ValueError("No query method defined for this search type")

        query_method = selected_type["query_method"]

        if not hasattr(self, query_method):
            AttributeError("Query method does not exist")

        return getattr(self, query_method)

    def search(
        self, search_type, search_value, fuzzy_search=False
    ) -> List[dict]:
        """High level search method

        Fetches query generator based on the `search_type` by
        calling `get_query_method`.

        Please see the `search_type_map` attribute
        for more information on the available types.

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
        # Pad 'itr' to length 'n' by appending 0 or more 'pad's.
        def tuple_pad(itr, n, pad):
            return itr + (pad,) * (n - len(itr))

        # Default processor simply returns the _source directly
        def default_processor(document):
            return document["_source"]

        # Get the query generator method
        query_method = self.get_query_method(search_type)

        # Prepare query and processor
        index, query, processor = tuple_pad(
            # Generate query
            query_method(search_value, fuzzy_search),
            # Pad with default_processor if no processor was returned
            3,
            default_processor,
        )

        response = self.db.search(index=index, body=query)

        return [processor(document) for document in response["hits"]["hits"]]

    def _query_match(
        self,
        search_field: str,
        search_value: str,
        size: int,
        source_filter: list,
    ) -> dict:
        """Generate a query to match full names/keywords.

        Consider the following search:
            search_value = "ba"

        Searching by prefix would yield the following results:
            * banana
            * batman
            * Ali baba
            * The little bakery

        This type of query will only return results will a full match on
        keywords and is typically used as the initial search before attempting
        to broader searches.

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
            "_source": {"includes": list(source_filter)},
            "query": {"match": {search_field: search_value}},
        }

        return query

    def _query_match_phrase_prefix(
        self,
        search_field: str,
        search_value: str,
        size: int,
        source_filter: list,
    ) -> dict:
        """Generate a query to match on the search prefix.

        Unlike `match query` this is a broader search query,
        matching on everything that `starts with`.

        This is typically used as a second search attempt if there was no
        initial match.

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
            "_source": {"includes": list(source_filter)},
            "query": {"match_phrase_prefix": {search_field: search_value}},
        }

        return query

    def query_for_employee_by_name(
        self, name: str, fuzzy_search: bool
    ) -> Tuple[str, dict]:
        """Search query for an employee by the full name (passed as a string).

        For a regular search we are using a `multi_match` query in order to
        match the full name against the `name` and the `surname` fields,
        thus allowing the user to either search for a person by a full name,
        only the first name or the last name.

        Example:
            Searching for `Picard` will yield the following matches:
            * Jean Luc Picard
            * Robert Picard
            * Mario Picardo

        When performing a fuzzy search we are extending the same
        search principle but with a `bool` query where besides matching
        on the the (full) `name` string we are additionally matching
        on the last name prefix.

        Example:
            Searching for `Jean Picard` will yield the following matches:
            * Jean Luc Picard

            But not: Mario Picardo

        Args:
            name (str): Name of the document field to search in.
            fuzzy_search (bool): Search wider if True

        Returns:
            Tuple[str, dict]: Index name (str) and Elastic search query (dict)

        """

        index = "employees"

        source_filter = ["uuid", "name", "addresses.PHONE"]

        if fuzzy_search:
            # Split name in order to retrieve lastname(ish)
            names = name.split(" ")
            lastname = names[-1]
            query = {
                "_source": {"includes": list(source_filter)},
                "query": {
                    "bool": {
                        "must": [{"match": {"name": name}}],
                        "should": [
                            {"match_phrase_prefix": {"surname": lastname}}
                        ],
                    }
                },
            }
        else:
            query = {
                "_source": {"includes": list(source_filter)},
                "query": {
                    "multi_match": {
                        "query": str(name),
                        "type": "phrase_prefix",
                        "fields": ["surname", "name"],
                    }
                },
            }

        return (index, query)

    def query_for_employee_by_phone(
        self, phone_number: str, fuzzy_search: bool
    ) -> Tuple[str, dict]:
        """Search query for an employee by phone number.

        We are using a regular token match or a phrase prefix match.
        This mean we are trying to match the entire value.

        Example:
            Search value `22722222` will match the following only:
            * 22722222

        A fuzzy query will use `phrase_prefix` matching in order to match on
        the given prefix, the search for `2272` will yield following results:
            * 22722222
            * 22723333
            * 22724444

        But will not match
            * 43227233
            * 44442272

        Args:
            phone_number (str): Phone number, e.g. 21223344.
            fuzzy_search (bool): Search wider if True.

        Returns:
            Tuple[str, dict]: Index name (str) and Elastic search query (dict)

        """

        index = "employees"
        search_field = "addresses.PHONE.value"

        source_filter = ["uuid", "name", "addresses.PHONE"]

        if fuzzy_search:
            query = self._query_match_phrase_prefix(
                search_field, phone_number, 15, source_filter
            )
        else:
            query = self._query_match(
                search_field, phone_number, 15, source_filter
            )

        return (index, query)

    def query_for_employee_by_email(
        self, email_address: str, fuzzy_search: bool
    ) -> Tuple[str, dict]:
        """Search query for an employee by email address.

        We are only using `phrase_prefix` matching for email addresses.
        As a consequence, it is not possible to search by domain, e.g.
        `@example.com`.

        Search value `picard` will yield the following results:
        * picard@example.com
        * picard@starfleet.com

        But will not match:
        * info@picard.com

        Args:
            email_address (str): Email address, e.g. mail@example.com.
            fuzzy_search (bool): Search wider if True.

        Returns:
            Tuple[str, dict]: Index name (str) and Elastic search query (dict)

        """

        index = "employees"
        search_field = "addresses.EMAIL.value"

        source_filter = ["uuid", "name", "addresses.EMAIL"]

        query = self._query_match_phrase_prefix(
            search_field, email_address, 15, source_filter
        )
        return (index, query)

    def query_for_employee_by_engagement(
        self, engagement: str, fuzzy_search: bool
    ):
        """Search query for an engagement

        We are using `phrase_prefix` to match the engagement keyword.

        The search value `deck` will match:
        * deckhand
        * deck officer

        But will not match:
        * Officer on deck

        Args:
            engagement (str): Name of the engagement, e.g. `Deck officer`
            fuzzy_search (bool): Search wider if True.

        Returns:
            Tuple[str, dict]: Index name (str) and Elastic search query (dict)

        """

        index = "employees"

        search_field = "engagements.title"

        source_filter = ["uuid", "name", "engagements"]

        query = self._query_match_phrase_prefix(
            search_field, engagement, 15, source_filter
        )
        return (index, query)

    def query_for_org_unit_by_name(self, name: str, fuzzy_search: bool):
        """Search query for an org unit by name.

        We are using `phrase_prefix` to match the organisation unit by name.

        The search value `Me` will match:
        * Medical Room
        * Messhall

        But will not match:
        * Visitor Meetingpoint

        Args:
            name (str): Name of the org unit, e.g. `Command bridge`
            fuzzy_search (bool): Search wider if True.

        Returns:
            Tuple[str, dict]: Index name (str) and Elastic search query (dict)

        """

        index = "org_units"
        search_field = "name"

        source_filter = ["uuid", "name", "addresses"]

        query = self._query_match_phrase_prefix(
            search_field, name, 15, source_filter
        )
        return (index, query)

    def query_for_org_unit_by_kle(self, kle: str, fuzzy_search: bool):
        """Search query for an org unit by kle.

        Args:
            kle (str): KLE number or name.
            fuzzy_search (bool): Search wider if True.

        Returns:
            Tuple[str, dict]: Index name (str) and Elastic search query (dict)

        """

        index = "org_units"
        search_field = "kles.title"

        source_filter = ["uuid", "name"]
        #
        #        if fuzzy_search:
        #            query = self._query_match_phrase_prefix(
        #                search_field, kle, 15, source_filter
        #            )
        #        else:
        #            query = self._query_match(
        #                search_field, kle, 15, source_filter
        #            )

        query = {
            "size": 15,
            "_source": {"includes": list(source_filter)},
            "query": {
                "nested": {
                    "path": "kles",
                    "inner_hits": {"_source": ["kles.title"]},
                    "query": {"match_phrase_prefix": {search_field: kle}},
                }
            },
        }

        def processor(document):
            # Fetch nested query result
            kles = [
                subdocument["_source"]
                for subdocument in document["inner_hits"]["kles"]["hits"][
                    "hits"
                ]
            ]
            # Embed nested query result within root query result
            org_unit = document["_source"]
            org_unit["kles"] = kles
            return org_unit

        return (index, query, processor)

    def delete_index(self, index: str) -> dict:
        """Delete an entire index by name

        Args:
            index (str): Name of the index

        Returns:
            dict: Elasticsearch json response as dictionary

        """

        response = self.db.indices.delete(index=index, ignore=[400, 404])

        return response

    def create_index(self, index: str, mapping: dict) -> dict:

        response = self.db.indices.create(index=index, body=mapping)
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

    def bulk_insert_index(self, index: str, generator) -> dict:
        """Insert documents into a datastore index

        Args:
            index (str): Name of the index
            generator (func): Generator function, generating dicts.

        Returns:
            int, int: Number of documents indexed, documents processed.

        """
        indexed = 0
        total = 0
        for ok, action in streaming_bulk(
            client=self.db, index=index, actions=generator()
        ):
            indexed += ok
            total += 1

        return indexed, total
