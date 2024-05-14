from datetime import datetime, timezone, timedelta
import json

import pytest

from router.api.usecase import ItemListResult
from router.html.param import ItemListGetForm
from router.html.usecase import ItemListInHTML
from router.html.usecase.itemlist_in_html import ItemListInHTMLResultFactory
from router.html.usecase.shared import util as sutil, htmlname
from externalfacade.items import ItemFactory


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
            "router.html.usecase.itemlist_in_html.httpx.AsyncClient.post",
            return_value=DummyRequestResult(return_value=[]),
        )
        itemlistgetform = ItemListGetForm()
        res = await ItemListInHTML(
            api_url="dummy", local_timezone=sutil.JST, itemlistgetform=itemlistgetform
        ).execute()
        comparing_data = ItemListInHTMLResultFactory.create(
            itemlistgetform=itemlistgetform,
            items=[],
            error_msg=htmlname.HTMLViewError.NOT_RESULT_API.jname,
        )
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
            "router.html.usecase.itemlist_in_html.httpx.AsyncClient.post",
            return_value=DummyRequestResult(
                return_value=json.loads(get_res.model_dump_json())
            ),
        )
        itemlistgetform = ItemListGetForm()
        res = await ItemListInHTML(
            api_url="dummy", local_timezone=sutil.JST, itemlistgetform=itemlistgetform
        ).execute()
        comparing_data = ItemListInHTMLResultFactory.create(
            **get_res.model_dump(),
            itemlistgetform=itemlistgetform,
        )
        assert comparing_data == res
        d = datetime.now(timezone.utc)
        offset = d - d.replace(tzinfo=sutil.JST)
        for i in res.items:
            assert i.created_at.utcoffset() == offset
            assert i.updated_at.utcoffset() == offset
            if i.expiry_date:
                i.expiry_date.utcoffset() == offset
