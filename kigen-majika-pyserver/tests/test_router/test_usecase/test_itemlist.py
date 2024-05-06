from datetime import datetime, timezone

import pytest

from router.usecase import itemlist
from model.service import ItemDictRepository
from model.domain import Item, ItemFactory
from router.param import ItemRequestParam
from .shared import ItemComparingData


class TestItemList:

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
    async def test_get_all_one(self, test_db):
        data: dict[int, Item] = {}
        item = self.get_item(id=1)
        data[1] = item
        ret = await itemlist.ItemList(repository=ItemDictRepository(data)).get_all()
        assert len(ret.items) == 1
        assert ItemComparingData(**item.model_dump()) == ItemComparingData(
            **ret.items[0].model_dump()
        )

    @pytest.mark.asyncio
    async def test_get_all_three(self, test_db):
        data: dict[int, Item] = {}
        for i in range(1, 4):
            item = self.get_item(id=i)
            data[i] = item
        ret = await itemlist.ItemList(repository=ItemDictRepository(data)).get_all()
        assert len(ret.items) == 3
        for r in ret.items:
            assert ItemComparingData(**data[r.id].model_dump()) == ItemComparingData(
                **r.model_dump()
            )

    @pytest.mark.asyncio
    async def test_get_one_exist_data(self, test_db):
        data: dict[int, Item] = {}
        target_index = 1
        item = self.get_item(id=target_index)
        data[target_index] = item
        ret = await itemlist.ItemList(repository=ItemDictRepository(data)).get_one(
            itemrequestparam=ItemRequestParam(id=target_index)
        )
        assert len(ret.items) == 1
        assert ItemComparingData(**item.model_dump()) == ItemComparingData(
            **ret.items[0].model_dump()
        )

    @pytest.mark.asyncio
    async def test_get_one_not_found_data(self, test_db):
        data: dict[int, Item] = {}
        not_target_index = 2
        target_index = 1
        item = self.get_item(id=not_target_index)
        data[not_target_index] = item
        ret = await itemlist.ItemList(repository=ItemDictRepository(data)).get_one(
            itemrequestparam=ItemRequestParam(id=target_index)
        )
        assert len(ret.items) == 0
