from time import sleep
from typing import Iterator
from os2phonebook import helpers
from os2phonebook import datastore


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
    port = int(config["ELASTICSEARCH_PORT"])

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
