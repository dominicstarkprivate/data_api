import flask
import flask_restful
from data_api import database
from data_api import db_models
import marshmallow
from typing import Tuple
from data_api import errors
from data_api import helpers


class DataSchema(marshmallow.Schema):
    """Marshmallow schema for the POST request body of the /data entpoint.
    """
    text = marshmallow.fields.Str(required=True, allow_none=False)
    language = marshmallow.fields.Str(required=True, allow_none=False)


class ConsentSchema(marshmallow.Schema):
    """Marshmallow schema for the POST request body of the /consents endpoint.
    """
    consent = marshmallow.fields.Bool(required=True, allow_none=False)


class Data(flask_restful.Resource):
    """Data endpoint, where data can be submitted to.
    """

    def _parse_post_body(self) -> Tuple[str, str]:
        """Parse the request body of the post request and return the result.

        Returns:
            Tuple[str, str]: Returns the text and the language in the following
                order: (text, language).
        """
        if (flask.request.headers.get("Content-Type") != "application/json"):
            raise errors.ContentTypeNotJsonError(
                "Content type not supported. Must be 'application/json'.")

        request_json = flask.request.json or {}
        schema = DataSchema()
        _ = schema.load(request_json)
        return request_json["text"], request_json["language"]

    def post(self, customer_id: str, dialog_id: str) -> flask.Response:
        """Post request at /data/<customer_id>/<dialog_id> to save a new
        customer text in the db.

        Args:
            customer_id (str): Customer id.
            dialog_id (str): Dialog id.

        Returns:
            flask.Response: Flask response object.
        """
        text, language = self._parse_post_body()
        dialogs_from_different_customers = db_models.Text.query.filter_by(
            dialog_id=dialog_id).filter(
                db_models.Text.customer_id != customer_id).first()
        if dialogs_from_different_customers is not None:
            raise errors.DialogCustomerRelationError(
                f"Dialog with id '{dialog_id}' exists already for "
                "another customer. Each dialog is assigned to exactly one "
                "customer.")
        text_db_entry = db_models.Text(
            text, language, customer_id, dialog_id)
        database.db_session.add(text_db_entry)
        database.db_session.commit()
        return helpers.make_response(200)

    def get(self) -> flask.Response:
        """GET request at /data to receive customer texts. Query parameters
        are passed to the SQLAlchemy query.

        Returns:
            flask.Response: Flask response object. Contains the list of data
                items that the query returned.
        """
        texts = db_models.Text.query.filter_by(consent=True).filter_by(
            **flask.request.args.to_dict()).order_by(
                db_models.Text.creation_date.desc()).all()
        texts_json = [
            {"id": text.id, "text": text.text, "language": text.language,
             "creation_date": text.creation_date,
             "customer_id": text.customer_id, "dialog_id": text.dialog_id}
            for text in texts
        ]
        return helpers.make_response(200, data={"texts": texts_json})


class Consent(flask_restful.Resource):
    """Consent endpoint to give consent for usage for analytics purposes.
    """

    def _parse_post_body(self) -> bool:
        """Parse the request body of the post request and return the result.

        Returns:
            bool: Returns the consent flag.
        """
        if (flask.request.headers.get("Content-Type") != "application/json"):
            raise errors.ContentTypeNotJsonError(
                "Content type not supported. Must be 'application/json'.")

        request_json = flask.request.json or {}
        schema = ConsentSchema()
        _ = schema.load(request_json)
        return request_json["consent"]

    def post(self, dialog_id: str) -> flask.Response:
        """Post request at /constents/<dialog_id>. If the request payload is
        {'consent': True}, all data entries with the given dialog id are
        updated with consent=True, otherwise, they are deleted.

        Args:
            dialog_id (str): Dialog id of texts that should be updated or
                deleted.

        Returns:
            flask.Response: Flask response object.
        """
        consent = self._parse_post_body()
        dialogs = db_models.Text.query.filter_by(dialog_id=dialog_id)
        if dialogs.first() is None:
            raise errors.DialogNotFoundError(
                f"Dialog with id '{dialog_id}' does not exist.")
        if consent:
            dialogs.update(dict(consent=True))
        else:
            dialogs.delete()
        database.db_session.commit()
        return helpers.make_response(200)
