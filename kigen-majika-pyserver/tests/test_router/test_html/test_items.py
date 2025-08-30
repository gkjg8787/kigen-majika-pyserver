from datetime import datetime, timezone
import json

import pytest

from fastapi.testclient import TestClient

from main import app
from router.html.param import (
    AddItemPostForm,
    AddJanCodePostForm,
    EditItemGetForm,
    EditItemPostForm,
    DeleteItemPostForm,
    ItemListGetForm,
)
from router.html.usecase import (
    AddItemFormResult,
    AddJanCodeFormResult,
    EditItemFormResult,
    DeleteItemFormResult,
)
from router.html.usecase.shared import htmlname
from router.html.usecase.itemlist_in_html import ItemListInHTMLResultFactory

client = TestClient(app)
prefix = "/items"


def is_html(text):
    assert "<!DOCTYPE html>" in text
    assert "<head>" in text
    assert "</head>" in text
    assert "<body>" in text
    assert "</body" in text
    assert "</html>" in text


@pytest.mark.anyio
async def test_read_users_items(test_db, mocker):
    itemlistgetform = ItemListGetForm()
    m1 = mocker.patch(
        "router.html.usecase.itemlist_in_html.ItemListInHTML.execute",
        return_value=ItemListInHTMLResultFactory.create(
            itemlistgetform=itemlistgetform, items=[]
        ),
    )
    response = client.get(f"{prefix}/", params=itemlistgetform.model_dump_json())
    assert response.status_code == 200
    is_html(response.text)
    assert "カメラで検索" in response.text


@pytest.mark.anyio
async def test_read_users_items_read_jancode(test_db, mocker):
    response = client.get(f"{prefix}/readjancode")
    assert response.status_code == 200
    is_html(response.text)
    assert "JANコード読み取り" in response.text
    assert "interactive" in response.text # for quagga
    assert "quagga.min.js" in response.text


@pytest.mark.anyio
async def test_read_users_items_add_jancode(test_db, mocker):
    response = client.get(f"{prefix}/add/jancode")
    assert response.status_code == 200
    is_html(response.text)
    assert "カメラを起動" in response.text

    # test with jan_code query param
    test_jan_code = "1234567890123"
    response = client.get(f"{prefix}/add/jancode?jan_code={test_jan_code}")
    assert response.status_code == 200
    is_html(response.text)
    assert f'value="{test_jan_code}"' in response.text


@pytest.mark.anyio
async def test_read_users_items_add(test_db, mocker):
    jancodeinfo_dict = {
        "jan_code": "0123456789012",
        "name": "test",
        "category": "none",
        "manufacturer": "maker",
    }
    addjancoderesult = AddJanCodeFormResult(is_next_page=False, **jancodeinfo_dict)
    m1 = mocker.patch(
        "router.html.usecase.additemform.AddJanCodeForm.execute",
        return_value=addjancoderesult,
    )
    addjancodepostform = AddJanCodePostForm(jan_code=jancodeinfo_dict["jan_code"])
    response = client.post(f"{prefix}/add/", data=addjancodepostform.model_dump())
    assert response.status_code == 200
    is_html(response.text)


@pytest.mark.anyio
async def test_read_users_items_add_post(test_db, mocker):
    name = "test"
    jan_code = "0123456789012"
    additemresult = AddItemFormResult(is_next_page=True, name=name, jan_code=jan_code)
    m1 = mocker.patch(
        "router.html.usecase.additemform.AddItemForm.execute",
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
    post_data = {
        k: v for k, v in additempostform.model_dump().items() if v is not None
    }
    response = client.post(f"{prefix}/add/result/", data=post_data)
    assert response.status_code == 200
    is_html(response.text)


@pytest.mark.anyio
async def test_read_users_items_edit(test_db, mocker):
    target_id = 1
    edititemgetform = EditItemGetForm(id=str(target_id))
    m1 = mocker.patch(
        "router.html.usecase.edititemform.EditItemInitForm.execute",
        return_value=EditItemFormResult(id=target_id),
    )
    response = client.get(
        f"{prefix}/edit/", params=json.loads(edititemgetform.model_dump_json())
    )
    assert response.status_code == 200
    is_html(response.text)


@pytest.mark.anyio
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
        "router.html.usecase.edititemform.EditItemForm.execute",
        return_value=EditItemFormResult(
            is_next_page=True, **edititempostform.model_dump()
        ),
    )
    response = client.post(
        f"{prefix}/edit/result/", data=edititempostform.model_dump()
    )
    assert response.status_code == 200
    is_html(response.text)


@pytest.mark.anyio
async def test_read_users_items_delete(test_db, mocker):
    target_id = 1
    deleteitempostform = DeleteItemPostForm(id=str(target_id), name="")
    m1 = mocker.patch(
        "router.html.usecase.deleteitemform.DeleteItemInitForm.execute",
        return_value=DeleteItemFormResult(id=target_id),
    )
    response = client.post(f"{prefix}/delete/", data=deleteitempostform.model_dump())
    assert response.status_code == 200
    is_html(response.text)


@pytest.mark.anyio
async def test_read_users_items_delete_result(test_db, mocker):
    target_id = 1
    deleteitempostform = DeleteItemPostForm(id=str(target_id), name="test")
    m1 = mocker.patch(
        "router.html.usecase.deleteitemform.DeleteItemForm.execute",
        return_value=DeleteItemFormResult(id=target_id, name="test", is_next_page=True),
    )
    response = client.post(
        f"{prefix}/delete/result/",
        data=deleteitempostform.model_dump(),
    )
    assert response.status_code == 200
    is_html(response.text)
