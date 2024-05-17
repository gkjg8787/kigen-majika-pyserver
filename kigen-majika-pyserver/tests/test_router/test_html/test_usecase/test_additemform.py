from datetime import datetime, timezone
import json

import pytest

from router.api.usecase import ItemCreateResult
from router.html.usecase import (
    AddItemForm,
    AddItemFormResult,
    AddJanCodeForm,
    AddJanCodeFormResult,
)
from router.html.param import AddItemPostForm, AddJanCodePostForm
from router.html.usecase.shared import htmlname
from domain.models import JanCodeInfo
from externalfacade.items import JanCodeInfoFactory
from application.items import IJanCodeInfoCreator

from . import shared


class DummyRequestResult:
    return_value: any

    def __init__(self, return_value: any):
        self.return_value = return_value

    def json(self):
        return self.return_value


class DummyJanCodeInfoCreator(IJanCodeInfoCreator):
    name: str
    category: str
    manufacturer: str
    updated_at: datetime

    def __init__(
        self,
        name: str = "",
        category: str = "",
        manufacturer: str = "",
        updated_at: datetime | None = None,
    ):
        self.name = name
        self.category = category
        self.manufacturer = manufacturer
        if not updated_at:
            self.updated_at = datetime.now(timezone.utc)
        else:
            self.updated_at = updated_at

    async def create(self, jan_code: str) -> JanCodeInfo:
        return JanCodeInfoFactory.create(
            jan_code=jan_code,
            name=self.name,
            category=self.category,
            manufacturer=self.manufacturer,
            updated_at=self.updated_at,
        )


class TestAddJanCodeForm:
    @pytest.mark.asyncio
    async def test_execute_get_jancodeinfo(self, mocker):
        id = 1
        item = shared.get_item(id=id)
        name = "test"
        addjancodepostform = AddJanCodePostForm(jan_code=item.jan_code)
        addjancodeformresult = await AddJanCodeForm(
            jancodeinfocreator=DummyJanCodeInfoCreator(name=name),
            addjancodepostform=addjancodepostform,
        ).execute()
        comparing_data = AddJanCodeFormResult(
            is_next_page=False, name=name, jan_code=item.jan_code
        )
        assert comparing_data == addjancodeformresult


class TestAddItemForm:

    @pytest.mark.asyncio
    async def test_execute_create(self, mocker):
        id = 1
        name = "test"
        item = shared.get_item(id=id, name=name)
        additempostform = AddItemPostForm(
            name="",  # None here to go find the name
            jan_code=item.jan_code,
            inventory=item.inventory,
            place=item.place,
            category=item.category,
            manufacturer=item.manufacturer,
            text=item.text,
            expiry_date=item.expiry_date,
            local_timezone=htmlname.LocalTimeZone.JST,
        )

        icr = ItemCreateResult(item=item, error_msg="")
        m2 = mocker.patch(
            "router.html.usecase.additemform.httpx.AsyncClient.post",
            return_value=DummyRequestResult(
                return_value=json.loads(icr.model_dump_json())
            ),
        )
        create_url = "dummy"
        additemformresult = await AddItemForm(
            additempostform=additempostform,
            create_url=create_url,
        ).execute()
        comparing_data = AddItemFormResult(
            is_next_page=True, name=name, jan_code=item.jan_code
        )
        assert comparing_data == additemformresult
