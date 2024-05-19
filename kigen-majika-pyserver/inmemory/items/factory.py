from datetime import datetime

from domain.models import (
    IItemFactory,
    IJanCodeInfoFactory,
    Item,
    JanCodeInfo,
    JanCode,
    IJanCodeFactory,
)


class InMemoryItemFactory(IItemFactory):
    @classmethod
    def create(
        cls,
        id: int,
        name: str,
        jan_code: JanCode,
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


class InMemoryJanCodeFactory(IJanCodeFactory):
    @classmethod
    def create(cls, jan_code: str) -> JanCode:
        return JanCode(value=jan_code)


class InMemoryJanCodeInfoFactory(IJanCodeInfoFactory):
    @classmethod
    def create(
        cls,
        jan_code: JanCode,
        name: str,
        category: str,
        manufacturer: str,
        updated_at: datetime,
    ) -> JanCodeInfo:
        return JanCodeInfo(
            jan_code=jan_code,
            name=name,
            category=category,
            manufacturer=manufacturer,
            updated_at=updated_at,
        )
