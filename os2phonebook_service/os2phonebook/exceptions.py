# There is really no need for a seperate module
#
# The rationale behind is to allow for expansion
# but mainly to adhere to the common namespace for custom exceptions
#
# Example:
#   from os2phonebook.exceptions import InvalidRequestBody, InvalidSearchType
#

class InvalidCredentials(Exception):
    """Request body is not valid according to the given schema"""
    status_code = 401


class InsufficientCredentials(Exception):
    """Request body is not valid according to the given schema"""
    status_code = 403


class InvalidCredentials(Exception):
    """Request body is not valid according to the given schema"""

    status_code = 401


class InsufficientCredentials(Exception):
    """Request body is not valid according to the given schema"""

    status_code = 403


class InvalidCredentials(Exception):
    """Request body is not valid according to the given schema"""

    status_code = 401


class InsufficientCredentials(Exception):
    """Request body is not valid according to the given schema"""

    status_code = 403


class InvalidRequestBody(Exception):
    """Request body is not valid according to the given schema"""

    status_code = 400


class InvalidSearchType(Exception):
    """Search type is not supported"""

    status_code = 400
