"""Collection of Documents API endpoints."""

from flask import Blueprint, request

from src.connection import session
from src.documents.models import RevisionModel, TitleModel
from src.documents.schema import (
    RevisionsPostRequestSchema,
    RevisionsSchema,
    TitleSchema
)
from src.utils import deserialize_request, serialize_response

documents = Blueprint("documents", __name__)


@documents.route("/documents", methods=['GET'])
def get_all_titles():
    query = session.query(TitleModel).all()
    return serialize_response(query, TitleSchema)


@documents.route("/documents/<title>", methods=['GET', 'POST'])
def get_revisions_by_title(title):
    if request.method == "GET":
        query = RevisionModel.get_query_with_titles(session)
        query = query.filter(
            TitleModel.title == title
        )
        return serialize_response(query, RevisionsSchema)
    elif request.method == "POST":
        payload = request.json
        validation, errors = deserialize_request(payload, RevisionsPostRequestSchema)
        if errors:
            return validation

        title = TitleModel.get_or_create_title(session, title)
        if isinstance(title, dict):
            return title
        new_review = RevisionModel(**validation, title_id=title.id)
        session.add(new_review)
        session.commit()
        return serialize_response(new_review, RevisionsPostRequestSchema, many=False), 201


@documents.route("/documents/<title>/<timestamp>", methods=['GET'])
def get_revisions_by_title_and_timestamp(title, timestamp):
    validation, errors = deserialize_request({
        "title": title,
        "timestamp": timestamp,
    }, RevisionsSchema)
    if errors:
        return validation
    query = RevisionModel.get_query_with_titles(session)
    query = query.filter(
        TitleModel.title == title,
        RevisionModel.timestamp <= timestamp
    ).order_by(
        RevisionModel.timestamp.desc()
    ).first()
    return serialize_response(query, RevisionsSchema, many=False)


@documents.route("/documents/<title>/latest", methods=['GET'])
def get_title_by_latest_revision(title):
    query = RevisionModel.get_query_with_titles(session)
    query = query.filter(
        TitleModel.title == title
    ).order_by(
        RevisionModel.timestamp.desc()
    ).first()
    return serialize_response(query, RevisionsSchema, many=False)
