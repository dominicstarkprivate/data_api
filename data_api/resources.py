import flask
import flask_restful
import sqlite3
from data_api import constants


def get_db_connection() -> sqlite3.Connection:
    """Get sql lite db connection object, that acts as an interface for
    database actions.
    """
    connection = sqlite3.connect(constants.DB_FILENAME)
    connection.row_factory = sqlite3.Row
    return connection


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
        db_connection = get_db_connection()
        text_id = 0
        cursor = db_connection.cursor()
        cursor.execute(
            "INSERT INTO texts (text_id, text, language, customer_id, "
            "dialog_id) VALUES (?, ?, ?, ?, ?)",
            (text_id, text, language, 0, 0))
        db_connection.commit()
        cursor.close()
        db_connection.close()
        return flask.make_response(
            {"message": "Sucess.", "data": {"id": text_id}}, 200)

    def get(self) -> flask.Response:
        """GET request at /data to receive customer texts.
        """
        db_connection = get_db_connection()
        texts = db_connection.execute('SELECT * FROM texts').fetchall()
        texts = [dict(t) for t in texts]
        db_connection.close()
        return flask.make_response(
            {"message": "Success.", "data": {"texts": texts}}, 200)


class Consent(flask_restful.Resource):
    """Consent endpoint to give consent for usage for analytics purposes.
    """

    def post(self) -> flask.Response:
        """Post request at /data to save a new customer text in the db.
        """
        return flask.make_response({"Message": "Sucess."}, 200)
