from datetime import datetime, timezone
import json
import copy

import pytest

from fastapi.testclient import TestClient

from main import app
from model.domain import ItemFactory, JanCodeInfoFactory
from router.param import (
    ItemCreateParam,
    ItemUpdateParam,
    ItemDeleteParam,
    ItemRequestParam,
)
from router.usecase import (
    ItemListResult,
    JanCodeInfoResult,
    ItemCreateResult,
    ItemUpdateResult,
    ItemDeleteResult,
)

client = TestClient(app)
prefix = "/api"


@pytest.mark.asyncio
async def test_read_api_items_no_data(test_db, mocker):
    m = mocker.patch(
        "router.usecase.ItemList.get",
        return_value=ItemListResult(items=[]),
    )
    response = client.post(f"{prefix}/items/", json={})
    assert response.status_code == 200
    assert response.json() == ItemListResult().model_dump()


def create_item(id: int, expiry_date: datetime | None = None):
    now = datetime.now(timezone.utc)
    jan_code = str(id)
    name = f"test{id}"
    return ItemFactory.create(
        id=id,
        name=name,
        jan_code=jan_code,
        inventory=1,
        place="other",
        category="not category",
        manufacturer="not manufacturer",
        text="memo",
        expiry_date=expiry_date,
        created_at=now,
        updated_at=now,
    )


@pytest.mark.asyncio
async def test_read_api_items_one_data(test_db, mocker):
    item = create_item(id=1)
    m = mocker.patch(
        "router.usecase.ItemList.get",
        return_value=ItemListResult(items=[item]),
    )
    response = client.post(f"{prefix}/items/", json={})
    assert response.status_code == 200
    assert response.json() == json.loads(ItemListResult(items=[item]).model_dump_json())


@pytest.mark.asyncio
async def test_read_api_items_three_data(test_db, mocker):

    itemlist = [create_item(id=1), create_item(id=2), create_item(id=3)]
    m = mocker.patch(
        "router.usecase.ItemList.get",
        return_value=ItemListResult(items=copy.deepcopy(itemlist)),
    )
    response = client.post(f"{prefix}/items/", json={})
    assert response.status_code == 200
    assert response.json() == json.loads(
        ItemListResult(items=itemlist).model_dump_json()
    )


@pytest.mark.asyncio
async def test_read_api_item_detail_no_data(test_db, mocker):
    target_id = 1
    irp = ItemRequestParam(id=target_id)
    m = mocker.patch(
        "router.usecase.ItemOne.get",
        return_value=ItemListResult(items=[]),
    )
    response = client.post(
        f"{prefix}/items/detail/", json=json.loads(irp.model_dump_json())
    )
    assert response.status_code == 200
    assert response.json() == ItemListResult().model_dump()


@pytest.mark.asyncio
async def test_read_api_item_detail_exist_data(test_db, mocker):
    target_id = 1
    item = create_item(id=target_id)
    irp = ItemRequestParam(id=target_id)
    m = mocker.patch(
        "router.usecase.ItemOne.get",
        return_value=ItemListResult(items=[item]),
    )
    response = client.post(
        f"{prefix}/items/detail/", json=json.loads(irp.model_dump_json())
    )
    assert response.status_code == 200
    assert response.json() == json.loads(ItemListResult(items=[item]).model_dump_json())


@pytest.mark.asyncio
async def test_read_api_item_jancodeinfo_get_data(test_db, mocker):
    jan_code = "012456789012"
    name = "test"
    category = "category"
    manufacturer = "maker"
    updated_at = datetime.now(timezone.utc)
    jancodeinfo = JanCodeInfoFactory.create(
        jan_code=jan_code,
        name=name,
        category=category,
        manufacturer=manufacturer,
        updated_at=updated_at,
    )
    m = mocker.patch(
        "router.usecase.GetOnlineJanCodeInfo.get_or_create",
        return_value=JanCodeInfoResult(jancodeinfo=jancodeinfo),
    )
    response = client.get(f"{prefix}/items/{jan_code}/info/")
    assert response.status_code == 200
    assert response.json() == json.loads(
        JanCodeInfoResult(jancodeinfo=jancodeinfo).model_dump_json()
    )


@pytest.mark.asyncio
async def test_read_api_item_jancodeinfo_not_get_data(test_db, mocker):
    jan_code = "012456789012"
    m = mocker.patch(
        "router.usecase.GetOnlineJanCodeInfo.get_or_create",
        return_value=JanCodeInfoResult(),
    )
    response = client.get(f"{prefix}/items/{jan_code}/info/")
    assert response.status_code == 200
    assert response.json() == json.loads(JanCodeInfoResult().model_dump_json())


@pytest.mark.asyncio
async def test_read_api_item_create(test_db, mocker):
    icp = ItemCreateParam(name="test", jan_code="0123456789012")
    now = datetime.now(timezone.utc)
    item = ItemFactory.create(
        id=1,
        **icp.model_dump(),
        created_at=now,
        updated_at=now,
    )
    icr = ItemCreateResult(error_msg="", item=item)
    m = mocker.patch(
        "router.usecase.ItemCreate.create",
        return_value=icr,
    )
    response = client.post(
        f"{prefix}/items/create", json=json.loads(icp.model_dump_json())
    )
    assert response.status_code == 200
    assert response.json() == json.loads(icr.model_dump_json())


@pytest.mark.asyncio
async def test_read_api_item_update(test_db, mocker):
    iup = ItemUpdateParam(
        id=1,
        name="test",
        jan_code="0123456789012",
        inventory=2,
        place="other",
        category="no category",
        manufacturer="not manufacturer",
        text="memo",
        expiry_date=datetime(2024, 10, 15, 21, 0, 0, tzinfo=timezone.utc),
    )
    now = datetime.now(timezone.utc)
    item = ItemFactory.create(
        **iup.model_dump(),
        created_at=now,
        updated_at=now,
    )
    iur = ItemUpdateResult(error_msg="", item=item, is_update=True)
    m = mocker.patch(
        "router.usecase.ItemUpdate.update",
        return_value=iur,
    )
    response = client.post(
        f"{prefix}/items/update", json=json.loads(iup.model_dump_json())
    )
    assert response.status_code == 200
    assert response.json() == json.loads(iur.model_dump_json())


@pytest.mark.asyncio
async def test_read_api_item_delete(test_db, mocker):
    idp = ItemDeleteParam(id=1)
    idr = ItemDeleteResult(error_msg="")
    m = mocker.patch(
        "router.usecase.ItemDelete.delete",
        return_value=idr,
    )
    response = client.post(
        f"{prefix}/items/delete", json=json.loads(idp.model_dump_json())
    )
    assert response.status_code == 200
    assert response.json() == json.loads(idr.model_dump_json())
