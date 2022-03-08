"""Collection of utils functions used in the API endpoints."""

from typing import Tuple

from flask import Response, jsonify
from marshmallow import ValidationError
from marshmallow.schema import SchemaMeta


def deserialize_request(obj: dict, schema: SchemaMeta) -> Tuple[dict, bool]:
    """Validates and deserializes an input dictionary/JSON to an application-level data structure.

    :param obj: Dictionary/JSON to validate.
    :param schema: Marshmallow schema that validates the input.
    """
    try:
        return schema().load(obj), False
    except ValidationError as err:
        return err.messages, True


def serialize_response(obj: dict, schema: SchemaMeta = None, many: bool = True) -> Response:
    """Serialize object and returns flask response.

    :param obj: Dictionary/JSON to serialize.
    :param schema: Marshmallow schema that serializes the input.
    :param many: Equals to true when dealing with iterable collections of objects.
    """
    if schema:
        return jsonify(schema(many=many).dump(obj))
    else:
        return jsonify(obj)
