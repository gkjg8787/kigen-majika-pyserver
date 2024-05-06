from datetime import datetime, timezone, tzinfo
import json

import pytest

from router.usecase import (
    DeleteItemInitForm,
    DeleteItemForm,
    DeleteItemFormResult,
    ItemListResult,
    ItemDeleteResult,
)
from router.param import DeleteItemPostForm
from model.domain import ItemFactory
from router.usecase.shared import htmlname


class DummyRequestResult:
    return_value: any

    def __init__(self, return_value: any):
        self.return_value = return_value

    def json(self):
        return self.return_value


def get_item(
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


class TestDeleteItemInitForm:

    @pytest.mark.asyncio
    async def test_execute(self, test_db, mocker):
        target_id = 1
        deleteitempostform = DeleteItemPostForm(id=str(target_id), name="")
        now = datetime.now(timezone.utc)
        item = get_item(id=target_id, created_at=now, updated_at=now)
        itemlistresult = ItemListResult(items=[item])
        m1 = mocker.patch(
            "router.usecase.edititemform.httpx.AsyncClient.post",
            return_value=DummyRequestResult(
                return_value=json.loads(itemlistresult.model_dump_json())
            ),
        )
        result = await DeleteItemInitForm(
            deleteitempostform=deleteitempostform, detail_api_url="dummy"
        ).execute()
        comparing_data = DeleteItemFormResult(**item.model_dump())
        assert result == comparing_data


class TestDeleteItemForm:
    @pytest.mark.asyncio
    async def test_execute_delete(self, test_db, mocker):
        target_id = 1
        deleteitempostform = DeleteItemPostForm(id=str(target_id), name="")
        itemdeleteresult = ItemDeleteResult()
        m1 = mocker.patch(
            "router.usecase.edititemform.httpx.AsyncClient.post",
            return_value=DummyRequestResult(
                return_value=json.loads(itemdeleteresult.model_dump_json())
            ),
        )
        result = await DeleteItemForm(
            deleteitempostform=deleteitempostform, delete_api_url="dummy"
        ).execute()
        comparing_data = DeleteItemFormResult(
            **deleteitempostform.model_dump(), is_next_page=True
        )
        assert result == comparing_data
