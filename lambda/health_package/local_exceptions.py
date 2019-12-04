"""Define custom exceptions"""


class BadRequestError(Exception):
    """There is a problem with the user request"""


class ServerError(Exception):
    """There is a problem on the server side"""
