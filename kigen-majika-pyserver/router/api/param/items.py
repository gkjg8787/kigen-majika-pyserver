from datetime import datetime, timezone

from pydantic import BaseModel, field_validator


class ItemListRequestParam(BaseModel):
    isort: int = 0
    stock: int = 0


class ItemRequestParam(BaseModel):
    id: int


class ItemCreateParam(BaseModel):
    name: str | None = None
    jan_code: str
    inventory: int | None = None
    place: str | None = None
    category: str | None = None
    manufacturer: str | None = None
    text: str | None = None
    expiry_date: datetime | None = None

    @field_validator("expiry_date")
    @classmethod
    def toUtc(cls, v: datetime | None):
        if not v:
            return v
        return v.replace(tzinfo=timezone.utc)


class ItemUpdateParam(BaseModel):
    id: int
    name: str
    jan_code: str
    inventory: int
    place: str
    category: str
    manufacturer: str
    text: str
    expiry_date: datetime | None

    @field_validator("expiry_date")
    @classmethod
    def toUtc_expiry_date(cls, v: datetime | None):
        if not v:
            return v
        return v.replace(tzinfo=timezone.utc)


class ItemDeleteParam(BaseModel):
    id: int
