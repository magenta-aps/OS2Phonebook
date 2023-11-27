import os
import json
from logging import getLogger, Logger, Formatter
from logging.handlers import RotatingFileHandler


def config_factory():
    """
    Auto initiates config

    There are so few config parameters that it did not make
    sense creating an external configuration file

    The following parameters should be generated:

        * OS2PHONEBOOK_COMPANY_NAME
        * OS2PHONEBOOK_LOG_ROOT
        * ELASTICSEARCH_HOST
        * ELASTICSEARCH_PORT

    The following parameters are optional:

        * OS2PHONEBOOK_DATALOADER_USERNAME
        * OS2PHONEBOOK_DATALOADER_PASSWORD

    Raises:
        EnvironmentError:

    """
    # Prep dictionary for return
    configuration_dict = {}

    required_parameters = [
        "OS2PHONEBOOK_COMPANY_NAME",
        "OS2PHONEBOOK_LOG_ROOT",
        "ELASTICSEARCH_HOST",
        "ELASTICSEARCH_PORT",
    ]

    optional_parameters = {
        "OS2PHONEBOOK_DATALOADER_USERNAME": "dataloader",
        "OS2PHONEBOOK_DATALOADER_PASSWORD": None,
    }
    for parameter_name in required_parameters:
        parameter_value = os.getenv(parameter_name)

        if not parameter_value:
            raise EnvironmentError(
                f"MISSING_ENVIRONMENT_VARIABLE={parameter_name}"
            )

        configuration_dict[parameter_name] = parameter_value

    for parameter_name, default_value in optional_parameters.items():
        parameter_value = os.environ.get(parameter_name, default_value)
        if not parameter_value:
            continue
        configuration_dict[parameter_name] = parameter_value

    return configuration_dict


def log_factory(namespace: str = "os2phonebook") -> Logger:
    """Create an instance of the Logger class.

    Args:
        namespace (int): The logging namespace.
            The namespace defaults to "os2phonebook" and should never change,
            at least not in the scope of this application.

    Returns:
        An instance of the Logger class.

    """
    return getLogger(namespace)


def configure_logging(log_root: str, log_file: str, logger: Logger) -> None:
    """Configure existing Logger instance with a format and file handler.

    Args:
        log_root (str): An absolute path to logging directory.
            Example: /var/log/os2phonebook.
        log_file (str): The log filename.
            Example: service.log
        logger (Logger): An instance of the Logger class.

    Raises:
        TypeError: If the logger is not an instance of the Logger class.
            Otherwise setting up the format and handler will fail.
        FileNotFoundError: If the log_root directory does not already exist.

    """
    if not isinstance(logger, Logger):
        raise TypeError(
            "Function will only accept an instance of the python Logger class"
        )

    if not os.path.exists(log_root):
        raise FileNotFoundError("Specified log directory does not exist")

    # TODO: Must be passed through config module
    log_file_size = 1000000
    log_level = 20

    # DEFAULT TO INFO log level (10)
    logger.setLevel(log_level)

    # Log format
    log_format = Formatter("[%(asctime)s] %(levelname)s %(message)s")

    activity_log_file = os.path.join(log_root, log_file)

    # Setup handlers
    activity_log_handler = RotatingFileHandler(
        filename=activity_log_file, maxBytes=log_file_size
    )

    activity_log_handler.setFormatter(log_format)
    activity_log_handler.setLevel(log_level)

    logger.addHandler(activity_log_handler)


def dump_file(filename, data_as_dict) -> None:
    """
    Serialize dictionary to json file
    Helper function

    This is used to persist the imported
    organisation units and employees to disk in a json format.

    The reason for storing objects as json rather serialized python
    is to allow other components to transfer the data to
    elasticsearch.

    Args:
        filename (str): File destination (absolute)
        data_as_dict (dict): Dictionary/Map of organisation units and employees

    """

    with open(filename, "w") as file:
        content = json.dumps(data_as_dict)
        file.write(content)


def load_file(filename) -> dict:
    """
    Load json formatted file as dictionary
    Helper function

    This is used to export the previously imported content
    to the elasticsearch backend.

    Args:
        filename (str): Absolute path to a source (json) file

    Returns:
        dict: A map of organisation units and employees as a dictionary.

    """

    with open(filename, "r") as file:
        content = file.read()
        data_as_dict = json.loads(content)

    return data_as_dict
