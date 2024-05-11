from datetime import datetime, timezone
import json

import pytest

from fastapi.testclient import TestClient

from main import app
from router.usecase import (
    AddItemFormResult,
    ItemListInHTMLResult,
    EditItemFormResult,
    DeleteItemFormResult,
)
from router.param import (
    AddItemPostForm,
    EditItemGetForm,
    EditItemPostForm,
    DeleteItemPostForm,
    ItemListGetForm,
)
from router.usecase.shared import htmlname, htmlform
from router.usecase.html.itemlist_in_html import ItemListInHTMLResultFactory

client = TestClient(app)
prefix = "/items"


def is_html(text):
    assert "<!DOCTYPE html>" in text
    assert "<head>" in text
    assert "</head>" in text
    assert "<body>" in text
    assert "</body" in text
    assert "</html>" in text


@pytest.mark.asyncio
async def test_read_users_items(test_db, mocker):
    itemlistgetform = ItemListGetForm()
    m1 = mocker.patch(
        "router.usecase.html.itemlist_in_html.ItemListInHTML.execute",
        return_value=ItemListInHTMLResultFactory.create(
            itemlistgetform=itemlistgetform, items=[]
        ),
    )
    response = client.get(f"{prefix}/", params=itemlistgetform.model_dump_json())
    assert response.status_code == 200
    is_html(response.text)


@pytest.mark.asyncio
async def test_read_users_items_add(test_db, mocker):
    response = client.get(f"{prefix}/add/")
    assert response.status_code == 200
    is_html(response.text)


@pytest.mark.asyncio
async def test_read_users_items_add_post(test_db, mocker):
    name = "test"
    jan_code = "0123456789012"
    additemresult = AddItemFormResult(is_next_page=True, name=name, jan_code=jan_code)
    m1 = mocker.patch(
        "router.usecase.html.additemform.AddItemForm.execute",
        return_value=additemresult,
    )
    additempostform = AddItemPostForm(
        name=name,
        jan_code=jan_code,
        inventory=0,
        place="",
        category="",
        manufacturer="",
        text="",
        expiry_date=None,
        local_timezone=additemresult.local_timezone,
    )
    response = client.post(
        f"{prefix}/add/result/", data=json.loads(additempostform.model_dump_json())
    )
    assert response.status_code == 200
    is_html(response.text)


@pytest.mark.asyncio
async def test_read_users_items_edit(test_db, mocker):
    target_id = 1
    edititemgetform = EditItemGetForm(id=str(target_id))
    m1 = mocker.patch(
        "router.usecase.html.edititemform.EditItemInitForm.execute",
        return_value=EditItemFormResult(id=target_id),
    )
    response = client.get(
        f"{prefix}/edit/", params=json.loads(edititemgetform.model_dump_json())
    )
    assert response.status_code == 200
    is_html(response.text)


@pytest.mark.asyncio
async def test_read_users_items_edit_post(test_db, mocker):
    target_id = 1
    edititempostform = EditItemPostForm(
        id=str(target_id),
        name="test",
        jan_code=str(target_id),
        inventory=2,
        place="testplace",
        category="testcategory",
        manufacturer="testmanufacturer",
        text="testtext",
        expiry_date=datetime(2026, 1, 2),
        local_timezone=htmlname.LocalTimeZone.JST,
    )
    m1 = mocker.patch(
        "router.usecase.html.edititemform.EditItemForm.execute",
        return_value=EditItemFormResult(
            is_next_page=True, **edititempostform.model_dump()
        ),
    )
    response = client.post(
        f"{prefix}/edit/result/", data=json.loads(edititempostform.model_dump_json())
    )
    assert response.status_code == 200
    is_html(response.text)


@pytest.mark.asyncio
async def test_read_users_items_delete(test_db, mocker):
    target_id = 1
    deleteitempostform = DeleteItemPostForm(id=str(target_id), name="")
    m1 = mocker.patch(
        "router.usecase.html.deleteitemform.DeleteItemInitForm.execute",
        return_value=DeleteItemFormResult(id=target_id),
    )
    response = client.post(
        f"{prefix}/delete/", data=json.loads(deleteitempostform.model_dump_json())
    )
    assert response.status_code == 200
    is_html(response.text)


@pytest.mark.asyncio
async def test_read_users_items_delete_result(test_db, mocker):
    target_id = 1
    deleteitempostform = DeleteItemPostForm(id=str(target_id), name="test")
    m1 = mocker.patch(
        "router.usecase.html.deleteitemform.DeleteItemForm.execute",
        return_value=DeleteItemFormResult(id=target_id, name="test", is_next_page=True),
    )
    response = client.post(
        f"{prefix}/delete/result/",
        data=json.loads(deleteitempostform.model_dump_json()),
    )
    assert response.status_code == 200
    is_html(response.text)
