"""Definitions of Marshmallow models schema used to validate/serialize."""

from datetime import datetime

from marshmallow import Schema, fields, pre_load
from marshmallow.validate import Length


class RevisionsSchema(Schema):
    """Schema for Revision model."""
    timestamp = fields.DateTime()

    class Meta:
        fields = (
            "revision",
            "title",
            "timestamp",
            "content",
        )

    @pre_load
    def date_to_datetime(self, data, *args, **kwargs) -> dict:
        """Allows to use date as query param."""
        try:
            if "timestamp" in data:
                data["timestamp"] = datetime.fromisoformat(
                    data["timestamp"]
                ).strftime("%Y-%m-%dT%H:%M:%S")
        except ValueError:
            pass
        return data


class RevisionsPostRequestSchema(RevisionsSchema):
    """Schema for Revision model's POST requests."""
    content = fields.String(required=True)


class TitleSchema(Schema):
    """Schema for Title model."""
    title = fields.String(validate=Length(max=50))

    class Meta:
        fields = (
            "title",
        )
