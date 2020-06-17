from flask import Flask
from os2phonebook import __version__
from os2phonebook.controller import api
from os2phonebook import helpers
from os2phonebook import datastore

# Init & configure logging
log = helpers.log_factory()


def initiate_application(config: dict) -> Flask:
    """Initiate and configure Flask instance

    Args:
        config (dict): A dictionary containing configuration

    Returns:
        :obj:`Flask`: An instance of flask
    """

    # Config parameters
    organisation_name = config["OS2PHONEBOOK_COMPANY_NAME"]
    db_host = config["ELASTICSEARCH_HOST"]
    db_port = config["ELASTICSEARCH_PORT"]

    log.info("INITIATE_SERVICE - Config parameters loaded")

    # Init flask instance
    app = Flask(import_name=__name__, static_url_path="")

    # Set metadata values
    app.os2phonebook_version = __version__
    app.organisation_name = organisation_name

    # Create datastore connection object
    app.connection = datastore.create_connection(db_host, db_port)
    log.info("INITIATE_SERVICE - Datastore connection created")

    # Blueprintes for api routes
    app.register_blueprint(api)

    log.info("INITIATE_SERVICE - Routes registered")

    log.info("INITIATE_SERVICE - Launching application service")
    return app
