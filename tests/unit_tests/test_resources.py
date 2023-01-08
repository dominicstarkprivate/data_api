import unittest
import json
import data_api.app
from data_api import database
from unittest import mock


class TestData(unittest.TestCase):

    def setUp(self):
        self.app = data_api.app.app
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///testing_db.db"
        self.test_client = self.app.test_client()
        return None

    def test_post__positive(self):
        # Act.
        response = self.test_client.post(
            "/data/1/2",
            data=json.dumps(
                {"text": "some text", "language": "some language"}),
            content_type="application/json")

        # Assert.
        response_data_json = json.loads(response.get_data(as_text=True))
        self.assertDictEqual(
            response_data_json, {"code": 200, "message": "Success."})
        return None

    def test_post__negative_application_context(self):
        # Act.
        response = self.test_client.post(
            "/data/1/2",
            data=json.dumps(
                {"text": "some text", "language": "some language"}),
            content_type="")

        # Assert.
        response_data_json = json.loads(response.get_data(as_text=True))
        self.assertDictEqual(
            response_data_json,
            {
                "code": 400,
                "message": "Content type not supported. Must be "
                "'application/json'."
            }
        )
        return None

    def test_post__negative_wrong_format(self):
        # Act.
        response = self.test_client.post(
            "/data/1/2",
            data=json.dumps({"text": ""}),
            content_type="application/json")

        # Assert.
        response_data_json = json.loads(response.get_data(as_text=True))
        self.assertDictEqual(
            response_data_json,
            {
                "code": 400,
                "message": "{'language': ['Missing data for required field.']}"
            }
        )
        return None

    def test_post__negative_dialog_relation(self):
        # Prepare.
        database.init_db()

        # Act.
        self.test_client.post(
            "/data/1/2",
            data=json.dumps({"text": "", "language": ""}),
            content_type="application/json")
        response = self.test_client.post(
            "/data/0/2",
            data=json.dumps({"text": "", "language": ""}),
            content_type="application/json")

        # Assert.
        response_data_json = json.loads(response.get_data(as_text=True))
        self.assertDictEqual(
            response_data_json,
            {
                "code": 409,
                "message": "Dialog with id '2' exists already for another "
                "customer. Each dialog is assigned to exactly one customer."
            }
        )
        return None

    def test_get__positive(self):
        # Prepare.
        database.init_db()

        # Act.
        self.test_client.post(
            "/data/1/2",
            data=json.dumps({"text": "", "language": ""}),
            content_type="application/json")
        self.test_client.post(
            "/data/1/1",
            data=json.dumps({"text": "", "language": ""}),
            content_type="application/json")
        self.test_client.post(
            "/consents/1",
            data=json.dumps({"consent": True}),
            content_type="application/json")
        response = self.test_client.get("/data")

        # Assert.
        response_data_json = json.loads(response.get_data(as_text=True))
        self.assertDictEqual(
            response_data_json,
            {
                "code": 200,
                "message": "Success.",
                "data": {
                    "texts": [{
                        "creation_date": mock.ANY,
                        "customer_id": "1",
                        "dialog_id": "1",
                        "id": 2,
                        "language": "",
                        "text": ""
                    }]
                }
            }
        )
        return None


class TestConsent(unittest.TestCase):

    def setUp(self):
        self.app = data_api.app.app
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///testing_db.db"
        self.test_client = self.app.test_client()
        return None

    def test_post__positive(self):
        # Prepare.
        database.init_db()

        # Act.
        self.test_client.post(
            "/data/1/2",
            data=json.dumps({"text": "", "language": ""}),
            content_type="application/json")
        response = self.test_client.post(
            "/consents/2",
            data=json.dumps({"consent": True}),
            content_type="application/json")

        # Assert.
        response_data_json = json.loads(response.get_data(as_text=True))
        self.assertDictEqual(
            response_data_json, {"code": 200, "message": "Success."})
        return None

    def test_post__positive_delete(self):
        # Prepare.
        database.init_db()

        # Act.
        self.test_client.post(
            "/data/1/2",
            data=json.dumps({"text": "", "language": ""}),
            content_type="application/json")
        response = self.test_client.post(
            "/consents/2",
            data=json.dumps({"consent": False}),
            content_type="application/json")

        # Assert.
        response_data_json = json.loads(response.get_data(as_text=True))
        self.assertDictEqual(
            response_data_json, {"code": 200, "message": "Success."})
        get_response = self.test_client.get("/data")
        get_response_data_json = json.loads(
            get_response.get_data(as_text=True))
        self.assertDictEqual(
            get_response_data_json,
            {
                "code": 200,
                "message": "Success.",
                "data": {
                    "texts": []
                }
            }
        )
        return None


if __name__ == "__main__":
    unittest.main()
