from datetime import datetime, timezone
import json

import pytest

from router.api.usecase import (
    ItemListResult,
    ItemDeleteResult,
)
from router.html.usecase import (
    DeleteItemInitForm,
    DeleteItemForm,
    DeleteItemFormResult,
)
from router.html.param import DeleteItemPostForm
from router.html.usecase.shared import util as sutil
from . import shared


class DummyRequestResult:
    return_value: any

    def __init__(self, return_value: any):
        self.return_value = return_value

    def json(self):
        return self.return_value


class TestDeleteItemInitForm:

    @pytest.mark.asyncio
    async def test_execute(self, test_db, mocker):
        target_id = 1
        deleteitempostform = DeleteItemPostForm(id=str(target_id), name="")
        now = datetime.now(timezone.utc)
        item = shared.get_item(id=target_id, created_at=now, updated_at=now)
        itemlistresult = ItemListResult(items=[item])
        m1 = mocker.patch(
            "router.html.usecase.edititemform.httpx.AsyncClient.post",
            return_value=DummyRequestResult(
                return_value=json.loads(itemlistresult.model_dump_json())
            ),
        )
        result = await DeleteItemInitForm(
            deleteitempostform=deleteitempostform,
            detail_api_url="dummy",
            local_timezone=sutil.JST,
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
            "router.html.usecase.edititemform.httpx.AsyncClient.post",
            return_value=DummyRequestResult(
                return_value=json.loads(itemdeleteresult.model_dump_json())
            ),
        )
        result = await DeleteItemForm(
            deleteitempostform=deleteitempostform,
            delete_api_url="dummy",
            local_timezone=sutil.JST,
        ).execute()
        comparing_data = DeleteItemFormResult(
            **deleteitempostform.model_dump(), is_next_page=True
        )
        assert result == comparing_data
