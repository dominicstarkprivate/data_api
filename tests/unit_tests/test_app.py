import unittest
import data_api.app
import flask


class TestCreateApp(unittest.TestCase):

    def test_create_app(self):
        # Act.
        returned_app = data_api.app.create_app()

        # Assert.
        self.assertIsInstance(returned_app, flask.Flask)
        self.assertEqual(
            returned_app.config.get("SQLALCHEMY_DATABASE_URI", None),
            "sqlite:///customer_texts.db")
        return None


if __name__ == "__main__":
    unittest.main()
