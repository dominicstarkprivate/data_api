import flask
from data_api import constants
from data_api import resources
from data_api import rest_api


def create_app() -> flask.Flask:
    """Create and return the flask app.

    Returns:
        flask.Flask: The created flask app.
    """
    app = flask.Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = \
        f"sqlite:///{constants.DB_FILENAME}"
    api = rest_api.RestAPI(app)
    api.add_resource(
        resources.Data, "/data", "/data/<customer_id>/<dialog_id>")
    api.add_resource(resources.Consent, "/consents/<dialog_id>")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host=constants.BACKEND_HOST, port=constants.BACKEND_PORT)
