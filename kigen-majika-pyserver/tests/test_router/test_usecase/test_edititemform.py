from datetime import datetime, timezone, tzinfo
import json

import pytest

from router.usecase import (
    EditItemForm,
    EditItemInitForm,
    EditItemFormResult,
    ItemListResult,
    ItemUpdateResult,
)
from router.param import EditItemGetForm, EditItemPostForm
from model.domain import ItemFactory
from router.usecase.shared import htmlname, readitemform


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


class TestEditItemInitForm:

    @pytest.mark.asyncio
    async def test_execute_exist_data(self, test_db, mocker):
        target_id = 1
        edititemgetform = EditItemGetForm(id=str(target_id))
        now = datetime.now(timezone.utc)
        item = get_item(id=target_id, created_at=now, updated_at=now)
        m1 = mocker.patch(
            "router.usecase.edititemform.GetOneItemForm.execute",
            return_value=readitemform.GetOneItemResult(item=item),
        )
        result = await EditItemInitForm(
            edititemgetform=edititemgetform, detail_api_url="dummy"
        ).execute()
        comparing_data = EditItemFormResult(**item.model_dump())
        assert result == comparing_data

    @pytest.mark.asyncio
    async def test_execute_not_found_data(self, test_db, mocker):
        target_id = 1
        edititemgetform = EditItemGetForm(id=str(target_id))
        error_msg = "Not Found Item"
        m1 = mocker.patch(
            "router.usecase.edititemform.GetOneItemForm.execute",
            return_value=readitemform.GetOneItemResult(error_msg=error_msg),
        )
        result = await EditItemInitForm(
            edititemgetform=edititemgetform, detail_api_url="dummy"
        ).execute()
        comparing_data = EditItemFormResult(id=target_id, error_msg=error_msg)
        assert result == comparing_data


class TestEditItemForm:

    def create_edititempostform(
        self,
        id: int,
        name: str = "",
        jan_code: str | None = None,
        inventory: int = 1,
        place: str = "",
        category: str = "",
        manufacturer: str = "",
        text: str = "",
        expiry_date: datetime | None = None,
        local_timezone: tzinfo = htmlname.LocalTimeZone.JST,
    ) -> EditItemPostForm:
        if not jan_code:
            jan_code = str(id)
        return EditItemPostForm(
            id=str(id),
            name=name,
            jan_code=jan_code,
            inventory=inventory,
            place=place,
            category=category,
            manufacturer=manufacturer,
            text=text,
            expiry_date=expiry_date,
            local_timezone=local_timezone,
        )

    @pytest.mark.asyncio
    async def test_execute_not_found_data(self, test_db, mocker):
        target_id = 1
        edititempostform = self.create_edititempostform(id=target_id)
        now = datetime.now(timezone.utc)
        itemupdateresult = ItemUpdateResult(
            is_update=False, error_msg=f"Not Found Data id={target_id}"
        )
        m1 = mocker.patch(
            "router.usecase.edititemform.httpx.AsyncClient.post",
            return_value=DummyRequestResult(
                return_value=json.loads(itemupdateresult.model_dump_json())
            ),
        )
        result = await EditItemForm(
            edititempostform=edititempostform,
            update_api_url="dummy",
            detail_api_url="dummy",
        ).execute()
        comparing_data = EditItemFormResult(
            id=target_id, is_next_page=True, error_msg="No Update"
        )
        assert result == comparing_data

    @pytest.mark.asyncio
    async def test_execute_update(self, test_db, mocker):
        target_id = 1
        edititempostform = self.create_edititempostform(id=target_id)
        item = get_item(id=target_id)
        itemupdateresult = ItemUpdateResult(is_update=True, item=item)
        m1 = mocker.patch(
            "router.usecase.edititemform.httpx.AsyncClient.post",
            return_value=DummyRequestResult(
                return_value=json.loads(itemupdateresult.model_dump_json())
            ),
        )
        result = await EditItemForm(
            edititempostform=edititempostform,
            update_api_url="dummy",
            detail_api_url="dummy",
        ).execute()
        comparing_data = EditItemFormResult(
            is_next_page=True, **itemupdateresult.item.model_dump()
        )
        assert result == comparing_data
