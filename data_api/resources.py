import flask
import flask_restful
from data_api import database
from data_api import db_models


class Data(flask_restful.Resource):
    """Data endpoint, where data can be submitted to.
    """

    def post(self, customer_id: int, dialog_id: int) -> flask.Response:
        """Post request at /data/<customer_id>/<dialog_id> to save a new
        customer text in the db.
        """
        customer_id = int(customer_id)
        dialog_id = int(dialog_id)
        content_type = flask.request.headers.get("Content-Type")
        if (content_type != "application/json"):
            raise ValueError(
                "Content type not supported. Must be 'application/json'.")
        data_item = flask.request.json
        if data_item is None:
            raise ValueError("Request body cannot be empty.")
        text = data_item["text"]
        language = data_item["language"]
        dialogs_from_different_customers = db_models.Text.query.filter_by(
            dialog_id=dialog_id).filter(
                db_models.Text.customer_id != customer_id).first()
        if dialogs_from_different_customers is not None:
            raise ValueError(
                f"Dialog with id '{dialog_id}' exists already for another "
                "customer. Each dialog is assigned to exactly one "
                "customer.")
        text_db_entry = db_models.Text(
            text, language, customer_id, dialog_id)
        database.db_session.add(text_db_entry)
        database.db_session.commit()
        return flask.make_response(
            {"message": "Success.", "data": {"id": text_db_entry.id}}, 200)

    def get(self) -> flask.Response:
        """GET request at /data to receive customer texts.
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
        return flask.make_response(
            {"message": "Success.", "data": {"texts": texts_json}}, 200)


class Consent(flask_restful.Resource):
    """Consent endpoint to give consent for usage for analytics purposes.
    """

    def post(self, dialog_id: int) -> flask.Response:
        """
        """
        dialog_id = int(dialog_id)
        payload = flask.request.json
        if payload is None:
            raise ValueError("Request body cannot be empty.")
        consent = payload.get("consent", False)
        if consent:
            db_models.Text.query.filter_by(dialog_id=dialog_id).update(
                dict(consent=True))
        else:
            db_models.Text.query.filter_by(
                dialog_id=dialog_id).delete()
        database.db_session.commit()
        return flask.make_response(
            {"message": "Success.", "data": {}}, 200)
