"""Create SQLAlchemy session to PostgreSQL."""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
session = Session(engine)
