"""Definition of the different tables in the db.
"""
import sqlalchemy as sqlal
from data_api.database import Base
import sqlalchemy.sql as sql


class Text(Base):  # type: ignore
    """DB table that contains the texts from the customer support interactions.
    """
    __tablename__ = "text"
    id = sqlal.Column("id", sqlal.Integer, primary_key=True)
    text = sqlal.Column(sqlal.Text)
    language = sqlal.Column(sqlal.String(100))
    customer_id = sqlal.Column(sqlal.String(100), nullable=False)
    dialog_id = sqlal.Column(sqlal.String(100), nullable=False)
    creation_date = sqlal.Column(
        sqlal.DateTime(timezone=True), server_default=sql.func.now())
    consent = sqlal.Column(sqlal.Boolean, default=False)

    def __init__(
            self, text: str, language: str, customer_id: str,
            dialog_id: str) -> None:
        """Constructor of the TextsTable class. Initializes all the attributes.

        Args:
            text (str): Text content.
            language (str): Language identifier (as given by the user of the
                API).
            customer_id (str): Customer id.
            dialog_id (str): Dialog id.
        """
        self.text = text
        self.language = language
        self.customer_id = customer_id
        self.dialog_id = dialog_id
        return None
