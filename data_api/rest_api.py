import flask_restful
import marshmallow
from data_api import errors
import logging
from data_api import helpers
import flask


class RestAPI(flask_restful.Api):
    """Child class of the flask restful Api class. We define this so that
    we can overwrite the handle_error function.
    """

    def handle_error(self, e: Exception) -> flask.Response:
        """This function overwrites the function 'handle_error' of the
        flask_restful.Api class. It allows us to do custom error handling.

        Args:
            e (Exception): Exception instance.

        Returns:
            flask.Response: Flask response object.
        """
        logging.exception(e)
        if isinstance(e, marshmallow.ValidationError):
            return helpers.make_response(400, message=str(e))
        elif isinstance(e, errors.ContentTypeNotJsonError):
            return helpers.make_response(400, message=str(e))
        elif isinstance(e, errors.DialogCustomerRelationError):
            return helpers.make_response(409, message=str(e))
        elif isinstance(e, errors.DialogNotFoundError):
            return helpers.make_response(404, message=str(e))
        else:
            return helpers.make_response(500, message="Internal server error.")
