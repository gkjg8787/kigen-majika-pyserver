from datetime import datetime, timezone, timedelta

from fastapi import Form

from pydantic import BaseModel


def toUtc(base: datetime, local_timezone: str):
    if not local_timezone:
        return base.replace(tzinfo=timezone.utc)
    HOUR = 0
    MINUTE = 1
    SECOND = 2
    timearray = local_timezone.split(":")
    if not timearray:
        return base.replace(tzinfo=timezone.utc)
    t = timedelta(hours=int(timearray[HOUR]))
    if len(timearray) > MINUTE:
        t += timedelta(minutes=int(timearray[MINUTE]))
    if len(timearray) > SECOND:
        t += timedelta(seconds=int(timearray[SECOND]))
    return base.replace(tzinfo=timezone(t)).astimezone(timezone.utc)


class ItemListGetForm(BaseModel):
    isort: int = 0
    stock: int = 0

    def __init__(self, isort: str = "", stock: str = ""):
        super().__init__()
        if isort and isort.isdigit():
            self.isort = int(isort)
        if stock and stock.isdigit():
            self.stock = int(stock)


class AddItemPostForm(BaseModel):
    name: str | None
    jan_code: str
    inventory: int | None
    place: str | None
    category: str | None
    manufacturer: str | None
    text: str | None
    expiry_date: datetime | None
    local_timezone: str = ""

    def __init__(
        self,
        name: str | None = Form(None),
        jan_code: str = Form(),
        inventory: int | None = Form(None),
        place: str | None = Form(None),
        category: str | None = Form(None),
        manufacturer: str | None = Form(None),
        text: str | None = Form(None),
        expiry_date: datetime | None = Form(None),
        local_timezone: str = Form(""),
    ):
        super().__init__(
            name=name,
            jan_code=jan_code,
            inventory=inventory,
            place=place,
            category=category,
            manufacturer=manufacturer,
            text=text,
            expiry_date=expiry_date,
            local_timezone=local_timezone,
        )
        if self.expiry_date:
            self.expiry_date = toUtc(
                base=self.expiry_date, local_timezone=self.local_timezone
            )


class EditItemGetForm(BaseModel):
    id: int

    def __init__(self, id: str = ""):
        if id and id.isdigit():
            super().__init__(id=int(id))
        else:
            ValueError("id is not int")


class EditItemPostForm(BaseModel):
    id: int
    name: str | None
    jan_code: str
    inventory: int | None
    place: str | None
    category: str | None
    manufacturer: str | None
    text: str | None
    expiry_date: datetime | None
    local_timezone: str = ""

    def __init__(
        self,
        id: str = Form(),
        name: str | None = Form(None),
        jan_code: str = Form(),
        inventory: int | None = Form(None),
        place: str | None = Form(None),
        category: str | None = Form(None),
        manufacturer: str | None = Form(None),
        text: str | None = Form(None),
        expiry_date: datetime | None = Form(None),
        local_timezone: str = Form(""),
    ):
        if not name:
            name = ""
        if not inventory:
            inventory = 0
        if not place:
            place = ""
        if not category:
            category = ""
        if not manufacturer:
            manufacturer = ""
        if not text:
            text = ""
        super().__init__(
            id=int(id),
            name=name,
            jan_code=jan_code,
            inventory=inventory,
            place=place,
            category=category,
            manufacturer=manufacturer,
            text=text,
            expiry_date=expiry_date,
            local_timezone=local_timezone,
        )
        if self.expiry_date:
            self.expiry_date = toUtc(
                base=self.expiry_date, local_timezone=self.local_timezone
            )


class DeleteItemPostForm(BaseModel):
    id: int
    name: str

    def __init__(self, id: str = Form(), name: str = Form("")):
        if id and id.isdigit():
            super().__init__(id=int(id), name=name)
        else:
            ValueError("id is not int")
