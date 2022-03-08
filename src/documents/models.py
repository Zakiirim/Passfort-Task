import uuid
from datetime import datetime
from typing import Union

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, inspect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session

from src.documents.schema import TitleSchema
from src.utils import deserialize_request

Base = declarative_base()


class TitleModel(Base):
    """SQLAlchemy model for titles table."""
    __tablename__ = "titles"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)

    @classmethod
    def get_or_create_title(cls, session: Session, title: str, commit: bool = True) -> Union[dict, Base]:
        """Check if a title is mapped in titles tables and eventually maps it.

        :param session: SQLAlchemy session to use.
        :param title: Title to look for
        :param commit: If the newly created title need to be committed.
        """
        validation, errors = deserialize_request({"title": title}, TitleSchema)
        if errors:
            return validation
        title_obj = session.query(TitleModel).filter(
            TitleModel.title == validation["title"]
        ).first()
        if title_obj is None:
            title_obj = TitleModel(title=validation["title"])
            session.add(title_obj)
            if commit:
                session.commit()
            else:
                session.flush()

        return title_obj


class RevisionModel(Base):
    """SQLAlchemy model for revisions table."""
    __tablename__ = "revisions"

    revision = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime, default=datetime.now)
    content = Column(String, nullable=False)
    title_id = Column(ForeignKey("titles.id"))

    @classmethod
    def get_query_with_titles(cls, session) -> Query:
        """Returns the query with the title mapping.

        :param session: SQLAlchemy session to use.
        """
        revision_model = inspect(cls).tables[0]
        title_model = inspect(TitleModel).tables[0]
        revision_columns = list(revision_model.columns)
        title_columns = list(title_model.columns)
        output_cols = []
        for columns in (revision_columns, title_columns):
            output_cols.extend(columns)

        return session.query(*output_cols).filter(
            revision_model.c.title_id == title_model.c.id
        )
