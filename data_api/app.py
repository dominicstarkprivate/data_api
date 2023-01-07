import flask
from data_api import constants
import flask_restful
from data_api import resources

app = flask.Flask(__name__)
api = flask_restful.Api(app)

api.add_resource(resources.Data, "/data")
api.add_resource(resources.Consent, "/consent")


if __name__ == "__main__":
    app.run(host=constants.BACKEND_HOST, port=constants.BACKEND_PORT)
