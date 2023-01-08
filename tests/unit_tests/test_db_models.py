import unittest
from data_api import db_models


class TestText(unittest.TestCase):

    def test_init(self):
        # Prepare.
        text = "my_text"
        language = "my_language"
        customer_id = "my_customer_id"
        dialog_id = "my_dialog_id"

        # Act.
        db_entry = db_models.Text(text, language, customer_id, dialog_id)

        # Assert.
        self.assertEqual(db_entry.text, text)
        self.assertEqual(db_entry.language, language)
        self.assertEqual(db_entry.customer_id, customer_id)
        self.assertEqual(db_entry.dialog_id, dialog_id)
        self.assertIsNone(db_entry.creation_date)
        self.assertIsNone(db_entry.id)
        self.assertFalse(db_entry.consent)
        return None


if __name__ == "__main__":
    unittest.main()
