from fastapi import APIRouter, Request, Form, Depends, status, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse

from fastapi.templating import Jinja2Templates


from router.param import (
    ItemListGetForm,
    AddItemPostForm,
    EditItemGetForm,
    EditItemPostForm,
    DeleteItemPostForm,
)
from router.usecase import (
    AddItemFormResult,
    AddItemForm,
    ItemListInHTML,
    EditItemInitForm,
    EditItemForm,
    DeleteItemInitForm,
    DeleteItemForm,
)
from model.service.connect_api import ConnectToAPIJanCodeInfoCreator
from router.usecase.shared import util as s_util

router = APIRouter(prefix="/items", tags=["items"])
templates = Jinja2Templates(directory="templates")
templates.env.filters["toLocalTextFormat"] = s_util.toLocalTextFormat
templates.env.filters["toLocalExpiryDateTextFormat"] = (
    s_util.toLocalExpiryDateTextFormat
)


@router.get("/", response_class=HTMLResponse)
async def read_users_items(
    request: Request, itemlistgetform: ItemListGetForm = Depends()
):
    result = await ItemListInHTML(
        api_url=str(request.url_for("read_api_items")),
        local_timezone=s_util.JST,
        itemlistgetform=itemlistgetform,
    ).execute()
    ret = templates.TemplateResponse(
        request=request, name="users/itemlist.html", context=result.get_context()
    )
    return ret


@router.get("/add", response_class=HTMLResponse)
async def read_users_items_add(request: Request):
    context = AddItemFormResult().get_context()
    return templates.TemplateResponse(
        request=request,
        name="users/additem.html",
        context=context,
    )


@router.post("/add/result", response_class=HTMLResponse)
async def read_users_items_add_post(
    request: Request, additempostform: AddItemPostForm = Depends()
):

    result = await AddItemForm(
        jancodeinfocreator=ConnectToAPIJanCodeInfoCreator(
            url=str(
                request.url_for(
                    "read_api_item_jancodeinfo", jan_code=additempostform.jan_code
                )
            )
        ),
        additempostform=additempostform,
        create_url=str(request.url_for("read_api_item_create")),
    ).execute()
    context = result.get_context()
    return templates.TemplateResponse(
        request=request,
        name="users/additem.html",
        context=context,
    )


@router.get("/edit", response_class=HTMLResponse)
async def read_users_items_edit(
    request: Request, edititemgetform: EditItemGetForm = Depends()
):
    result = await EditItemInitForm(
        edititemgetform=edititemgetform,
        detail_api_url=str(request.url_for("read_api_item_detail")),
        local_timezone=s_util.JST,
    ).execute()
    context = result.get_context()
    return templates.TemplateResponse(
        request=request,
        name="users/edititem.html",
        context=context,
    )


@router.post("/edit/result", response_class=HTMLResponse)
async def read_users_items_edit_post(
    request: Request, edititempostform: EditItemPostForm = Depends()
):
    result = await EditItemForm(
        edititempostform=edititempostform,
        detail_api_url=str(request.url_for("read_api_item_detail")),
        update_api_url=str(request.url_for("read_api_item_update")),
        local_timezone=s_util.JST,
    ).execute()
    context = result.get_context()
    return templates.TemplateResponse(
        request=request,
        name="users/edititem.html",
        context=context,
    )


@router.post("/delete", response_class=HTMLResponse)
async def read_users_items_delete(
    request: Request, deleteitempostform: DeleteItemPostForm = Depends()
):
    result = await DeleteItemInitForm(
        deleteitempostform=deleteitempostform,
        detail_api_url=str(request.url_for("read_api_item_detail")),
        local_timezone=s_util.JST,
    ).execute()
    context = result.get_context()
    return templates.TemplateResponse(
        request=request,
        name="users/deleteitem.html",
        context=context,
    )


@router.post("/delete/result", response_class=HTMLResponse)
async def read_users_items_delete_result(
    request: Request, deleteitempostform: DeleteItemPostForm = Depends()
):
    result = await DeleteItemForm(
        deleteitempostform=deleteitempostform,
        delete_api_url=str(request.url_for("read_api_item_delete")),
        local_timezone=s_util.JST,
    ).execute()
    context = result.get_context()
    return templates.TemplateResponse(
        request=request,
        name="users/deleteitem.html",
        context=context,
    )
