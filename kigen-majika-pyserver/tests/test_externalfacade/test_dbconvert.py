from datetime import datetime, timezone


from externalfacade.items import dbconvert
from externalfacade.items import ItemFactory, JanCodeFactory
from externalfacade import (
    ItemInventory,
    ItemCategory,
    ItemMemo,
    ItemName,
    ItemManufacturer,
)


class TestItemToDBObject:
    @classmethod
    def create_item(
        cls,
        id: int,
        name: str = "test",
        jan_code: str | None = None,
        inventory: int = 0,
        place: str = "place",
        category: str = "category",
        manufacturer: str = "",
        text: str = "text",
        expiry_date: datetime | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        now = datetime.now(timezone.utc)
        if not jan_code:
            jan_code = str(id)
        if not created_at:
            created_at = now
        if not updated_at:
            updated_at = now
        return ItemFactory.create(
            id=id,
            name=name,
            jan_code=JanCodeFactory.create(jan_code=jan_code),
            inventory=inventory,
            place=place,
            category=category,
            manufacturer=manufacturer,
            text=text,
            expiry_date=expiry_date,
            created_at=created_at,
            updated_at=updated_at,
        )

    def test_toItemInventory(self):
        now = datetime.now(timezone.utc)
        expiry_date = datetime(2024, 12, 1, 0, 0, 0, tzinfo=timezone.utc)
        item = self.create_item(
            id=1,
            name="test",
            jan_code="1234567890123",
            inventory=1,
            place="not place",
            expiry_date=expiry_date,
            created_at=now,
            updated_at=now,
        )
        iinv = dbconvert.ItemToDBObject.toItemInventory(item)
        compinv = ItemInventory(
            id=1,
            jan_code="1234567890123",
            inventory=1,
            place="not place",
            expiry_date=expiry_date,
            created_at=now,
            updated_at=now,
        )
        assert iinv.id == compinv.id
        assert iinv.jan_code == compinv.jan_code
        assert iinv.inventory == compinv.inventory
        assert iinv.place == compinv.place
        assert iinv.expiry_date == compinv.expiry_date
        assert iinv.created_at == compinv.created_at
        assert iinv.updated_at == compinv.updated_at

    def test_toItemName(self):
        item = self.create_item(
            id=1,
            name="test",
            jan_code="1234567890123",
        )
        iname = dbconvert.ItemToDBObject.toItemName(item)
        compname = ItemName(
            jan_code="1234567890123",
            name="test",
        )
        assert iname.jan_code == compname.jan_code
        assert iname.name == compname.name

    def test_toItemCategory(self):
        item = self.create_item(
            id=1,
            jan_code="1234567890123",
            category="food",
        )
        icate = dbconvert.ItemToDBObject.toItemCategory(item)
        compcate = ItemCategory(
            jan_code="1234567890123",
            category="food",
        )
        assert icate.jan_code == compcate.jan_code
        assert icate.category == compcate.category

    def test_toItemManufacturer(self):
        item = self.create_item(id=1, jan_code="1234567890123", manufacturer="maker")
        imanu = dbconvert.ItemToDBObject.toItemManufacturer(item)
        compcate = ItemManufacturer(jan_code="1234567890123", manufacturer="maker")
        assert imanu.jan_code == compcate.jan_code
        assert imanu.manufacturer == compcate.manufacturer

    def test_toItemMemo(self):
        item = self.create_item(
            id=1,
            text="memo",
        )
        imemo = dbconvert.ItemToDBObject.toItemMemo(item)
        compmemo = ItemMemo(
            id=1,
            text="memo",
        )
        assert imemo.id == compmemo.id
        assert imemo.text == compmemo.text
