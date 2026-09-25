"""Request/response schemas for the JSON API, validated with pydantic."""

from datetime import UTC, datetime
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, StringConstraints

ShortText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]
LongText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


def as_utc(value: datetime) -> datetime:
    # SQLite returns naive datetimes (stored as UTC); Postgres returns the session's timezone.
    return value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)


UTCDatetime = Annotated[datetime, AfterValidator(as_utc)]


class StoryCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: ShortText
    topic: ShortText
    text: LongText
    author: ShortText


class StoryUpdate(BaseModel):
    """Partial update: only the fields that are sent are changed."""

    model_config = ConfigDict(extra="forbid")

    title: ShortText | None = None
    topic: ShortText | None = None
    text: LongText | None = None
    author: ShortText | None = None


class StorySummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    author: str
    created_at: UTCDatetime


class StoryDetail(StorySummary):
    topic: str
    text: str
    updated_at: UTCDatetime


class Page(BaseModel):
    page: int
    per_page: int
    total: int
    pages: int


class StoryList(BaseModel):
    stories: list[StorySummary]
    meta: Page


class PageParams(BaseModel):
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=20, ge=1)
