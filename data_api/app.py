import flask
from data_api import constants
import flask_restful
from data_api import resources


def create_app():
    app = flask.Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = \
        f"sqlite:///{constants.DB_FILENAME}"
    api = flask_restful.Api(app)
    api.add_resource(
        resources.Data, "/data", "/data/<customer_id>/<dialog_id>")
    api.add_resource(resources.Consent, "/consents/<dialog_id>")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host=constants.BACKEND_HOST, port=constants.BACKEND_PORT)
