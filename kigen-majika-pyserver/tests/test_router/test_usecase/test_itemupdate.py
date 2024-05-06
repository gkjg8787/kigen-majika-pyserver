from datetime import datetime, timezone

import pytest

from router.usecase import itemupdate
from router.param import ItemUpdateParam
from model.service import ItemDictRepository
from model.domain import Item, ItemFactory


from .shared import ItemComparingData


class TestItemUpdate:
    def get_item(self, id: int):
        now = datetime.now(timezone.utc)
        expiry_date = datetime(2024, 12, 30, 0, 0, 0, tzinfo=timezone.utc)
        return ItemFactory.create(
            id=id,
            name=f"test{id}",
            jan_code=str(id),
            inventory=1,
            place="other",
            category="category",
            manufacturer="manufacturer",
            text="text",
            expiry_date=expiry_date,
            created_at=now,
            updated_at=now,
        )

    @pytest.mark.asyncio
    async def test_update_not_update(self, test_db):
        item = self.get_item(id=1)
        iup = ItemUpdateParam(**item.model_dump())
        data: dict[int, Item] = {}
        data[item.id] = item
        ret = await itemupdate.ItemUpdate(
            itemfactory=ItemFactory(), itemrepository=ItemDictRepository(data)
        ).update(itemupdateparam=iup)
        assert ret.is_update == False
        assert ret.item is None

    async def update_and_assert(self, item: Item, iup: ItemUpdateParam):
        data: dict[int, Item] = {}
        data[item.id] = item
        ret = await itemupdate.ItemUpdate(
            itemfactory=ItemFactory(), itemrepository=ItemDictRepository(data)
        ).update(itemupdateparam=iup)
        assert ret.is_update == True
        assert ret.item is not None
        assert item.id == ret.item.id
        assert ItemComparingData(**iup.model_dump()) == ItemComparingData(
            **ret.item.model_dump()
        )

    @pytest.mark.asyncio
    async def test_update_name(self, test_db):
        item = self.get_item(id=1)
        iup = ItemUpdateParam(**item.model_dump())
        iup.name = "醤油"
        await self.update_and_assert(item=item, iup=iup)

    @pytest.mark.asyncio
    async def test_update_inventory(self, test_db):
        item = self.get_item(id=1)
        iup = ItemUpdateParam(**item.model_dump())
        iup.inventory = 5
        await self.update_and_assert(item=item, iup=iup)

    @pytest.mark.asyncio
    async def test_update_place(self, test_db):
        item = self.get_item(id=1)
        iup = ItemUpdateParam(**item.model_dump())
        iup.place = "倉庫"
        await self.update_and_assert(item=item, iup=iup)

    @pytest.mark.asyncio
    async def test_update_category(self, test_db):
        item = self.get_item(id=1)
        iup = ItemUpdateParam(**item.model_dump())
        iup.category = "米"
        await self.update_and_assert(item=item, iup=iup)

    @pytest.mark.asyncio
    async def test_update_manufacturer(self, test_db):
        item = self.get_item(id=1)
        iup = ItemUpdateParam(**item.model_dump())
        iup.manufacturer = "製造者"
        await self.update_and_assert(item=item, iup=iup)

    @pytest.mark.asyncio
    async def test_update_text(self, test_db):
        item = self.get_item(id=1)
        iup = ItemUpdateParam(**item.model_dump())
        iup.text = "要注意"
        await self.update_and_assert(item=item, iup=iup)

    @pytest.mark.asyncio
    async def test_update_expriy_date(self, test_db):
        item = self.get_item(id=1)
        iup = ItemUpdateParam(**item.model_dump())
        iup.expiry_date = datetime(2024, 10, 11, 12, 00, 00, tzinfo=timezone.utc)
        await self.update_and_assert(item=item, iup=iup)

    @pytest.mark.asyncio
    async def test_update_any_params(self, test_db):
        item = self.get_item(id=1)
        iup = ItemUpdateParam(**item.model_dump())
        iup.name = "木の棒"
        iup.inventory = 20
        iup.place = "庭"
        iup.category = "木材"
        iup.manufacturer = "森"
        iup.text = "70サイズ"
        iup.expiry_date = datetime(2025, 4, 26, 12, 00, 00, tzinfo=timezone.utc)
        await self.update_and_assert(item=item, iup=iup)
