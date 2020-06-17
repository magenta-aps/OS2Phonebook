from time import sleep
from typing import Iterator
from os2phonebook import helpers
from os2phonebook import datastore
from os2phonebook.integration import OS2MOImportClient


# Init & configure logging
log = helpers.log_factory()


def ping_datastore(config: dict, interval=5, max_attempts=15) -> Iterator[str]:
    """Check connection status to the datastore.

    This functionality is mainly used in a docker context
    in order to delay the application startup in the
    entrypoint until the elasticsearch container is responding.

    Args:
        config (dict): A dictionary containing configuration.
        interval (int): Time in between the connection attempts.
        max_attempts (int): The total amount of attempts to connect.

    Yields:
        str: Progress update messages.
            This will be displayed in a terminal rather than in a log file.

            Example output:

                Setting up a connection to the datastore
                Attempting to connect to datastore 0/120
                Attempting to connect to datastore 1/120
                Attempting to connect to datastore 2/120
                Attempting to connect to datastore 3/120
                Successfully connected to the datastore

    """

    # Configuration parameters
    host = config["ELASTICSEARCH_HOST"]
    port = config["ELASTICSEARCH_PORT"]

    connection_status = False

    yield "Setting up a connection to the datastore"

    db = datastore.create_connection(host, port)

    for retry in range(max_attempts):

        # Info
        yield f"Attempting to connect to datastore {retry}/{max_attempts}"

        # Ping datastore
        connection_status = db.ping()

        # Break the loop if a pong is returned
        if connection_status:
            yield "Successfully connected to the datastore"
            return

        # Hacky grace interval
        sleep(interval)

    yield f"Maxium attempts ({max_attempts})reached"


def import_from_os2mo(
    config: dict, employees_map_file: str, org_units_map_file: str
) -> None:
    """Import employees and organisation units from the OS2MO service api.

    Bootstrap the OS2MOImportClient `import_routine` method
    and write the hashmaps to disk as json files.

    Args:
        config (dict): A dictionary containing configuration.
        employees_map_file (str): Name of the employees output file
        org_units_map_file (str): Name of the org_units output file

    """

    # Configuration parameters
    base_url = config["OS2MO_SERVICE_URL"]
    token = config["OS2MO_API_TOKEN"]

    # Perform the actual import from OS2MO
    # This may take a while...
    log.info("IMPORT_FROM_OS2MO - Begin caching content")

    client = OS2MOImportClient(base_url)
    client.configure_access_token(token)
    employees, org_units = client.import_routine()

    # Write files to the cache directory
    log.info("IMPORT_FROM_OS2MO - Write content to disk")
    helpers.dump_file(employees_map_file, employees)
    helpers.dump_file(org_units_map_file, org_units)

    # Complete
    log.info("IMPORT_FROM_OS2MO - Cache procedure completed")


def store_cache(
    config: dict, employees_map_file: str, org_units_map_file: str
):
    """Store employees and organisation units in the datastore.

    Load hashmaps of employees and organsation units
    from cached json files and store their content in the datastore.

    Args:
        config (dict): A dictionary containing configuration.
        employees_map_file (str): Name of the employees output file
        org_units_map_file (str): Name of the org_units output file

    """
    host = config["ELASTICSEARCH_HOST"]
    port = config["ELASTICSEARCH_PORT"]

    # Reload files from cache
    log.info("STORE_CACHE - Reloading content from cache")
    employees = helpers.load_file(employees_map_file)
    org_units = helpers.load_file(org_units_map_file)

    # Connect to datastore
    connection = datastore.create_connection(host, port)
    db = datastore.DataStore(connection)

    # Destroy previously inserted data
    log.info("STORE_CACHE - Delete previous datastore indices")
    db.delete_index("org_units")
    db.delete_index("employees")

    # Insert into elastic search
    log.info("STORE_CACHE - Storing content in the datastore")

    for uuid, unit in org_units.items():
        response = db.insert_index(
            index="org_units", identifier=uuid, data=unit
        )
        log.debug(response)

    for uuid, employee in employees.items():
        response = db.insert_index(
            index="employees", identifier=uuid, data=employee
        )
        log.debug(response)

    log.info("STORE_CACHE - Store procedure completed")
