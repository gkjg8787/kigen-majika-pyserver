from datetime import datetime, timezone, timedelta
import json

import pytest

from router.usecase import ItemListInHTML, ItemListInHTMLResult, ItemListResult
from router.usecase.shared import util as sutil
from model.domain import ItemFactory


class DummyRequestResult:
    return_value: any

    def __init__(self, return_value: any):
        self.return_value = return_value

    def json(self):
        return self.return_value


class TestItemListInHTML:
    @pytest.mark.asyncio
    async def test_execute_no_data(self, test_db, mocker):
        m1 = mocker.patch(
            "router.usecase.additemform.httpx.AsyncClient.get",
            return_value=DummyRequestResult(return_value=[]),
        )
        res = await ItemListInHTML(api_url="dummy", local_timezone=sutil.JST).execute()
        comparing_data = ItemListInHTMLResult()
        assert comparing_data == res

    def get_item(
        self,
        id: int,
        expiry_date: datetime | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        now = datetime.now(timezone.utc)
        if not created_at:
            created_at = now
        if not updated_at:
            updated_at = now
        return ItemFactory.create(
            id=id,
            name=f"test{id}",
            jan_code=str(id),
            inventory=1,
            place="",
            category="",
            manufacturer="",
            text="",
            expiry_date=expiry_date,
            created_at=created_at,
            updated_at=updated_at,
        )

    @pytest.mark.asyncio
    async def test_execute_one_data(self, test_db, mocker):
        target_id = 1
        now = datetime.now(timezone.utc)
        items = [self.get_item(id=target_id, created_at=now, updated_at=now)]
        get_res = ItemListResult(items=items)
        m1 = mocker.patch(
            "router.usecase.additemform.httpx.AsyncClient.get",
            return_value=DummyRequestResult(
                return_value=json.loads(get_res.model_dump_json())
            ),
        )
        res = await ItemListInHTML(api_url="dummy", local_timezone=sutil.JST).execute()
        comparing_data = ItemListInHTMLResult(
            **get_res.model_dump(), items_length=len(get_res.items)
        )
        assert comparing_data == res
        d = datetime.now(timezone.utc)
        offset = d - d.replace(tzinfo=sutil.JST)
        for i in res.items:
            assert i.created_at.utcoffset() == offset
            assert i.updated_at.utcoffset() == offset
            if i.expiry_date:
                i.expiry_date.utcoffset() == offset
