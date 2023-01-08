"""Definition of the different tables in the db.
"""
import sqlalchemy as sqlal
from data_api.database import Base


class TextsTable(Base):  # type: ignore
    """DB table that contains the texts from the customer support interactions.
    """
    __tablename__ = 'texts_table'
    id = sqlal.Column("text_id", sqlal.Integer, primary_key=True)
    text = sqlal.Column(sqlal.String(100))
    language = sqlal.Column(sqlal.String(100))
    customer_id = sqlal.Column(sqlal.String(100))
    dialog_id = sqlal.Column(sqlal.String(100))

    def __init__(
            self, text: str, language: str, customer_id: str,
            dialog_id: str) -> None:
        """Constructor of the TextsTable class. Initializes all the attributes.
        """
        self.text = text
        self.language = language
        self.customer_id = customer_id
        self.dialog_id = dialog_id
        return None

    def __repr__(self):
        return f"<Text {self.text!r}>"
