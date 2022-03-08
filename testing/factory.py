"""A collection of function for testing purposes."""

import random
import string
import uuid
from datetime import datetime

from src.connection import session
from src.documents.models import RevisionModel, TitleModel


def make_string(length=100) -> str:
    """Generate random string

    :param int length: Length of the string to generate.
    :return: Random string.
    """
    return "".join(
        random.choice(string.ascii_lowercase) for _ in range(length)
    )


def make_revision(commit=False, **kwargs) -> RevisionModel:
    """Create Revision object.

    :param commit: True if you want to commit the object in DB.
    :param kwargs: sequence of arguments of the new Revision object.
    :return: RevisionModel object.
    """
    random_title = kwargs.get("title", make_string(length=10))
    title = TitleModel.get_or_create_title(session, random_title, commit=commit)
    revision = RevisionModel(
        revision=kwargs.get("revision", uuid.uuid4()),
        timestamp=kwargs.get("timestamp", datetime.now()),
        content=make_string(length=20),
        title_id=title.id,
    )
    session.add(revision)
    if commit:
        session.commit()
    return revision
