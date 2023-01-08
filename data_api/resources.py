import flask
import flask_restful
from data_api import database
from data_api import db_models


class Data(flask_restful.Resource):
    """Data endpoint, where data can be submitted to.
    """

    def post(self) -> flask.Response:
        """Post request at /data to save a new customer text in the db.
        """
        content_type = flask.request.headers.get("Content-Type")
        if (content_type != "application/json"):
            raise ValueError(
                "Content type not supported. Must be 'application/json'.")
        data_item = flask.request.json
        if data_item is None:
            raise ValueError("Request body cannot be empty.")
        text = data_item["text"]
        language = data_item["language"]
        customer_id = "0"
        dialog_id = "0"
        text_db_entry = db_models.TextsTable(
            text, language, customer_id, dialog_id)
        database.db_session.add(text_db_entry)
        database.db_session.commit()
        return flask.make_response(
            {"message": "Sucess.", "data": {"id": text_db_entry.id}}, 200)

    def get(self) -> flask.Response:
        """GET request at /data to receive customer texts.
        """
        texts = db_models.TextsTable.query.all()
        texts_json = [
            {"id": text.id, "text": text.text, "language": text.language}
            for text in texts
        ]
        return flask.make_response(
            {"message": "Success.", "data": {"texts": texts_json}}, 200)


class Consent(flask_restful.Resource):
    """Consent endpoint to give consent for usage for analytics purposes.
    """

    def post(self) -> flask.Response:
        """Post request at /data to save a new customer text in the db.
        """
        return flask.make_response({"Message": "Sucess."}, 200)
