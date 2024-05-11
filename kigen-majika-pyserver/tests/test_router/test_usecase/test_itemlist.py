from datetime import datetime, timezone

import pytest

from router.usecase import ItemList, ItemOne
from model.service import ItemDictRepository, ItemQueryDictService
from model.domain import Item, ItemFactory
from router.param import ItemRequestParam, ItemListRequestParam
from .shared import ItemComparingData


def get_item(id: int):
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


class TestItemList:

    @pytest.mark.asyncio
    async def test_get_all_one(self, test_db):
        data: dict[int, Item] = {}
        item = get_item(id=1)
        data[1] = item
        itemlistrequestparam = ItemListRequestParam()
        ret = await ItemList(itemqueryservice=ItemQueryDictService(data)).get(
            itemlistrequestparam=itemlistrequestparam
        )
        assert len(ret.items) == 1
        assert ItemComparingData(**item.model_dump()) == ItemComparingData(
            **ret.items[0].model_dump()
        )

    @pytest.mark.asyncio
    async def test_get_all_three(self, test_db):
        data: dict[int, Item] = {}
        for i in range(1, 4):
            item = get_item(id=i)
            data[i] = item
        itemlistrequestparam = ItemListRequestParam()
        ret = await ItemList(itemqueryservice=ItemQueryDictService(data)).get(
            itemlistrequestparam=itemlistrequestparam
        )
        assert len(ret.items) == 3
        for r in ret.items:
            assert ItemComparingData(**data[r.id].model_dump()) == ItemComparingData(
                **r.model_dump()
            )


class TestItemOne:
    @pytest.mark.asyncio
    async def test_get_one_exist_data(self, test_db):
        data: dict[int, Item] = {}
        target_index = 1
        item = get_item(id=target_index)
        data[target_index] = item
        ret = await ItemOne(repository=ItemDictRepository(data)).get(
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
        item = get_item(id=not_target_index)
        data[not_target_index] = item
        ret = await ItemOne(repository=ItemDictRepository(data)).get(
            itemrequestparam=ItemRequestParam(id=target_index)
        )
        assert len(ret.items) == 0
