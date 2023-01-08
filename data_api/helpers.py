import flask
from typing import Optional, Dict


def make_response(
        code: int, message: str = "Success.",
        data: Optional[Dict] = None) -> flask.Response:
    """Make a flask response with two keys 'message' and 'code'.

    Args:
        code (int): HTTP status code.
        message (st: Message. Defaults to success.
        data (Optional[Dict] = None): Response data. Defaults to None.
    """
    response_dict = {"message": message, "code": code}
    if data:
        response_dict["data"] = data
    return flask.make_response(response_dict)
