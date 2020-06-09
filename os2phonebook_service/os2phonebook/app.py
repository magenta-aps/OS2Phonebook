from flask import Flask, Response
from werkzeug.security import generate_password_hash
import os
from os2phonebook import __version__
from os2phonebook.controller import api
from os2phonebook import helpers
from os2phonebook import datastore

# Init & configure logging
log = helpers.log_factory()


def gen_user_map(config):
    """Generate a usermap for the dataload endpoints HTTP Basic Auth.

    Cached via @lru_cache / @cache, as the output is configured by
    environmental variables at start-up.

    If no environmental variables are defined, an empty usermap is returned,
    thus making the dataload endpoints effectively inaccessible.

    Returns:
        :obj:`map` from :obj:`string` to :obj:`string`:
            Username: pbkdf2 password
    """
    username = config.get("OS2PHONEBOOK_DATALOADER_USERNAME", None)
    password = config.get("OS2PHONEBOOK_DATALOADER_PASSWORD", None)
    # No password, no access
    if username is None or password is None:
        log.warning("No HTTP Basic Auth credentials configured thus dataload is disabled")
        return []
    return {
        username: generate_password_hash(password)
    }


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
    db_port = int(config["ELASTICSEARCH_PORT"])

    log.info("INITIATE_SERVICE - Config parameters loaded")

    # Init flask instance
    app = Flask(
        import_name=__name__,
        static_url_path=""
    )

    # Set metadata values
    app.os2phonebook_version = __version__
    app.organisation_name = organisation_name
    app.dataload_basic_auth = gen_user_map(config)

    # Create datastore connection object
    app.connection = datastore.create_connection(db_host, db_port)
    log.info("INITIATE_SERVICE - Datastore connection created")

    # Blueprintes for api routes
    app.register_blueprint(api)

    log.info("INITIATE_SERVICE - Routes registered")

    log.info("INITIATE_SERVICE - Launching application service")
    return app
