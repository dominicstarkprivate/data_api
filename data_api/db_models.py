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
    text = sqlal.Column(sqlal.String(100))
    language = sqlal.Column(sqlal.String(100))
    customer_id = sqlal.Column(sqlal.Integer, nullable=False)
    dialog_id = sqlal.Column(sqlal.Integer, nullable=False)
    creation_date = sqlal.Column(
        sqlal.DateTime(timezone=True), server_default=sql.func.now())
    consent = sqlal.Column(sqlal.Boolean, default=False)

    def __init__(
            self, text: str, language: str, customer_id: int,
            dialog_id: int) -> None:
        """Constructor of the TextsTable class. Initializes all the attributes.
        """
        self.text = text
        self.language = language
        self.customer_id = customer_id
        self.dialog_id = dialog_id
        return None

    def __repr__(self):
        return f"<text: {self.text!r}>"
