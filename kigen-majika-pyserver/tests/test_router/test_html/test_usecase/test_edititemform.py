from datetime import datetime, timezone, tzinfo
import json

import pytest

from router.api.usecase import ItemUpdateResult
from router.html.usecase import (
    EditItemForm,
    EditItemInitForm,
    EditItemFormResult,
)
from router.html.param import EditItemGetForm, EditItemPostForm
from router.html.usecase.shared import htmlname, readitemform, util as sutil
from . import shared


class DummyRequestResult:
    return_value: any

    def __init__(self, return_value: any):
        self.return_value = return_value

    def json(self):
        return self.return_value


class TestEditItemInitForm:

    @pytest.mark.asyncio
    async def test_execute_exist_data(self, test_db, mocker):
        target_id = 1
        edititemgetform = EditItemGetForm(id=str(target_id))
        now = datetime.now(timezone.utc)
        item = shared.get_item(id=target_id, created_at=now, updated_at=now)
        m1 = mocker.patch(
            "router.html.usecase.edititemform.GetOneItemForm.execute",
            return_value=readitemform.GetOneItemResult(item=item),
        )
        result = await EditItemInitForm(
            edititemgetform=edititemgetform,
            detail_api_url="dummy",
            local_timezone=sutil.JST,
        ).execute()
        comparing_data = EditItemFormResult(
            **item.model_dump(exclude={"jan_code"}), jan_code=item.jan_code.value
        )
        assert result == comparing_data

    @pytest.mark.asyncio
    async def test_execute_not_found_data(self, test_db, mocker):
        target_id = 1
        edititemgetform = EditItemGetForm(id=str(target_id))
        error_msg = "Not Found Item"
        m1 = mocker.patch(
            "router.html.usecase.edititemform.GetOneItemForm.execute",
            return_value=readitemform.GetOneItemResult(error_msg=error_msg),
        )
        result = await EditItemInitForm(
            edititemgetform=edititemgetform,
            detail_api_url="dummy",
            local_timezone=sutil.JST,
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
            "router.html.usecase.edititemform.httpx.AsyncClient.post",
            return_value=DummyRequestResult(
                return_value=json.loads(itemupdateresult.model_dump_json())
            ),
        )
        result = await EditItemForm(
            edititempostform=edititempostform,
            update_api_url="dummy",
            detail_api_url="dummy",
            local_timezone=sutil.JST,
        ).execute()
        comparing_data = EditItemFormResult(
            id=target_id, is_next_page=True, error_msg="No Update"
        )
        assert result == comparing_data

    @pytest.mark.asyncio
    async def test_execute_update(self, test_db, mocker):
        target_id = 1
        edititempostform = self.create_edititempostform(id=target_id)
        item = shared.get_item(id=target_id)
        itemupdateresult = ItemUpdateResult(is_update=True, item=item)
        m1 = mocker.patch(
            "router.html.usecase.edititemform.httpx.AsyncClient.post",
            return_value=DummyRequestResult(
                return_value=json.loads(itemupdateresult.model_dump_json())
            ),
        )
        result = await EditItemForm(
            edititempostform=edititempostform,
            update_api_url="dummy",
            detail_api_url="dummy",
            local_timezone=sutil.JST,
        ).execute()
        comparing_data = EditItemFormResult(
            is_next_page=True,
            **itemupdateresult.item.model_dump(exclude={"jan_code"}),
            jan_code=itemupdateresult.item.jan_code.value,
        )
        assert result == comparing_data
