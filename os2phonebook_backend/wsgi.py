"""WSGI entrypoint."""
import sys
from os2phonebook.app import initiate_application
from os2phonebook.helpers import log_factory, configure_logging, config_factory

try:
    # Initiate logging
    log = log_factory()

    # Load config parameters from file
    config = config_factory()

    # Configure logging
    log_root = config["OS2PHONEBOOK_LOG_ROOT"]
    configure_logging(log_root, "service.log", log)

except Exception as error:
    print(error)
    sys.exit(1)

finally:
    # Create application instance
    app = initiate_application(config)
