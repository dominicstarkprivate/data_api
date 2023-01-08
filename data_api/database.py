"""Note that this file is based on the following flask documenation page:
https://flask.palletsprojects.com/en/2.2.x/patterns/sqlalchemy/
"""
import sqlalchemy as sqlal
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from data_api import constants


engine = sqlal.create_engine(f"sqlite:///{constants.DB_FILENAME}")
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db() -> None:
    """
    Empty all tables of the database.
    """
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import data_api.db_models  # noqa
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
