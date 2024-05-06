from datetime import datetime, timezone

import pytest

from router.usecase import itemdelete
from router.param import ItemDeleteParam
from model.service import ItemDictRepository
from model.domain import Item, ItemFactory


from .shared import ItemComparingData


class TestItemDelete:
    @pytest.mark.asyncio
    async def test_delete_exist_data(self, test_db):
        now = datetime.now(timezone.utc)
        expiry_date = datetime(2024, 6, 20, 3, 0, 0, tzinfo=timezone.utc)
        data: dict[int, Item] = {}
        itemdel = itemdelete.ItemDelete(itemrepository=ItemDictRepository(data))
        item = ItemFactory.create(
            id=1,
            name="test",
            jan_code="0123456789012",
            inventory=1,
            place="台所",
            category="お菓子",
            manufacturer="駄菓子",
            text="25度以下で保存",
            expiry_date=expiry_date,
            created_at=now,
            updated_at=now,
        )
        data[item.id] = item
        await itemdel.delete(itemdeleteparam=ItemDeleteParam(id=item.id))
        assert len(data) == 0

    @pytest.mark.asyncio
    async def test_delete_not_found_data(self, test_db):
        now = datetime.now(timezone.utc)
        expiry_date = datetime(2024, 6, 20, 3, 0, 0, tzinfo=timezone.utc)
        data: dict[int, Item] = {}
        itemdel = itemdelete.ItemDelete(itemrepository=ItemDictRepository(data))
        item = ItemFactory.create(
            id=1,
            name="test",
            jan_code="0123456789012",
            inventory=1,
            place="台所",
            category="お菓子",
            manufacturer="駄菓子",
            text="25度以下で保存",
            expiry_date=expiry_date,
            created_at=now,
            updated_at=now,
        )
        data[item.id] = item
        target_id = 10
        await itemdel.delete(itemdeleteparam=ItemDeleteParam(id=target_id))
        assert len(data) == 1
