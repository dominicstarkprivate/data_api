import unittest
import json
import marshmallow
from data_api import rest_api
import flask
from data_api import errors
import data_api.app


class TestRestApi(unittest.TestCase):

    def setUp(self):
        self.app = data_api.app.app
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///testing_db.db"
        self.test_client = self.app.test_client()
        return None

    def test_handle_error__marshmallow(self):
        # Prepare.
        message = "some error"
        error = marshmallow.ValidationError(message)
        api = rest_api.RestAPI(self.app)

        # Act.
        with self.app.app_context():
            response = api.handle_error(error)

        # Assert.
        self.assertIsInstance(response, flask.Response)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertDictEqual(response_data, {"code": 400, "message": message})
        return None

    def test_handle_error__content_type(self):
        # Prepare.
        message = "some error"
        error = errors.ContentTypeNotJsonError(message)
        api = rest_api.RestAPI(self.app)

        # Act.
        with self.app.app_context():
            response = api.handle_error(error)

        # Assert.
        self.assertIsInstance(response, flask.Response)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertDictEqual(response_data, {"code": 400, "message": message})
        return None

    def test_handle_error__dialog_relation(self):
        # Prepare.
        message = "some error"
        error = errors.DialogCustomerRelationError(message)
        api = rest_api.RestAPI(self.app)

        # Act.
        with self.app.app_context():
            response = api.handle_error(error)

        # Assert.
        self.assertIsInstance(response, flask.Response)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertDictEqual(response_data, {"code": 409, "message": message})
        return None

    def test_handle_error__dialog_not_found(self):
        # Prepare.
        message = "some error"
        error = errors.DialogNotFoundError(message)
        api = rest_api.RestAPI(self.app)

        # Act.
        with self.app.app_context():
            response = api.handle_error(error)

        # Assert.
        self.assertIsInstance(response, flask.Response)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertDictEqual(response_data, {"code": 404, "message": message})
        return None

    def test_handle_error__500_error(self):
        # Prepare.
        message = "some error"
        error = Exception(message)
        api = rest_api.RestAPI(self.app)

        # Act.
        with self.app.app_context():
            response = api.handle_error(error)

        # Assert.
        self.assertIsInstance(response, flask.Response)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertDictEqual(
            response_data, {"code": 500, "message": "Internal server error."})
        return None


if __name__ == "__main__":
    unittest.main()
