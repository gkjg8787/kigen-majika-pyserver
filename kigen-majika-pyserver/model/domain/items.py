from datetime import datetime
from abc import ABCMeta, abstractmethod

from pydantic import BaseModel, field_validator


class ItemNameData(BaseModel):
    jan_code: str
    name: str


class ItemCategoryData(BaseModel):
    jan_code: str
    category: str


class ItemManufacturerData(BaseModel):
    jan_code: str
    manufacturer: str


class Item(BaseModel):
    id: int
    name: str = ""
    jan_code: str
    inventory: int = 0
    place: str = ""
    category: str = ""
    manufacturer: str = ""
    text: str = ""
    expiry_date: datetime | None = None
    created_at: datetime
    updated_at: datetime

    @field_validator("inventory")
    @classmethod
    def inventory_out_of_range(cls, v):
        try:
            vv = int(v)
        except ValueError as err:
            raise ValueError("cannot convert to int")
        if vv < 0:
            raise ValueError("less than 0")
        return v


class IItemFactory(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def create(
        cls,
        id: int,
        name: str,
        jan_code: str,
        inventory: int,
        place: str,
        category: str,
        manufacturer: str,
        text: str,
        expiry_date: datetime,
        created_at: datetime,
        updated_at: datetime,
    ) -> Item:
        pass


class ItemFactory(IItemFactory):
    @classmethod
    def create(
        cls,
        id: int,
        name: str,
        jan_code: str,
        inventory: int,
        place: str,
        category: str,
        manufacturer: str,
        text: str,
        expiry_date: datetime | None,
        created_at: datetime,
        updated_at: datetime,
    ) -> Item:
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
        return Item(
            id=id,
            name=name,
            jan_code=jan_code,
            inventory=inventory,
            place=place,
            category=category,
            manufacturer=manufacturer,
            text=text,
            expiry_date=expiry_date,
            created_at=created_at,
            updated_at=updated_at,
        )
