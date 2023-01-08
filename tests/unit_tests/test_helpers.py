import unittest
from data_api import helpers
import flask
import json
import data_api.app


class TestMakeResponse(unittest.TestCase):

    def setUp(self):
        self.app = data_api.app.app
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///testing_db.db"
        self.test_client = self.app.test_client()
        return None

    def test_make_response(self):
        # Prepare.
        code = 200
        message = "my_message"
        data = {"some": "data"}

        # Act.
        with self.app.app_context():
            response = helpers.make_response(code, message=message, data=data)

        # Assert.
        response_data = json.loads(response.get_data(as_text=True))
        self.assertDictEqual(
            response_data, {"code": code, "message": message, "data": data})
        return None

    def test_make_response__defaults(self):
        # Prepare.
        code = 200

        # Act.
        with self.app.app_context():
            response = helpers.make_response(code)

        # Assert.
        response_data = json.loads(response.get_data(as_text=True))
        self.assertDictEqual(
            response_data, {"code": code, "message": "Success."})
        return None


if __name__ == "__main__":
    unittest.main()
