from typing import Optional
from fastapi import APIRouter, Request, Form, Depends, status, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse

from fastapi.templating import Jinja2Templates


from .param import (
    ItemListGetForm,
    AddItemPostForm,
    AddJanCodePostForm,
    EditItemGetForm,
    EditItemPostForm,
    DeleteItemPostForm,
    DeleteItemBulkPostForm,
)
from .usecase import (
    AddItemFormResult,
    AddItemForm,
    AddJanCodeForm,
    ItemListInHTML,
    EditItemInitForm,
    EditItemForm,
    DeleteItemInitForm,
    DeleteItemForm,
    DeleteItemBulkForm,
)
from application.items.connect_api import ConnectToAPIJanCodeInfoCreator
from .usecase.shared import util as s_util
from externalfacade.items import JanCodeInfoFactory, JanCodeFactory

router = APIRouter(prefix="/items", tags=["items"])
templates = Jinja2Templates(directory="templates")
templates.env.filters["toLocalTextFormat"] = s_util.toLocalTextFormat
templates.env.filters["toLocalExpiryDateTextFormat"] = (
    s_util.toLocalExpiryDateTextFormat
)
templates.env.filters["is_expired"] = s_util.is_expired_for_itemlist_in_html
templates.env.filters["is_caution"] = s_util.is_caution_for_itemlist_in_html
templates.env.filters["is_somewhat_caution"] = (
    s_util.is_somewhat_caution_for_itemlist_in_html
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


@router.get("/delete_bulk", response_class=HTMLResponse)
async def read_users_items_delete_bulk(
    request: Request, itemlistgetform: ItemListGetForm = Depends()
):
    result = await ItemListInHTML(
        api_url=str(request.url_for("read_api_items")),
        local_timezone=s_util.JST,
        itemlistgetform=itemlistgetform,
    ).execute()
    ret = templates.TemplateResponse(
        request=request,
        name="users/delete_items_bulk.html",
        context=result.get_context(),
    )
    return ret


@router.post("/delete_bulk/result", response_class=HTMLResponse)
async def read_users_items_delete_bulk_result(
    request: Request, deleteitembulkpostform: DeleteItemBulkPostForm = Depends()
):
    await DeleteItemBulkForm(
        deleteitembulkpostform=deleteitembulkpostform,
        delete_api_url=str(request.url_for("delete_api_items_bulk")),
    ).execute()
    return RedirectResponse(
        url=request.url_for("read_users_items_delete_bulk"),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/readjancode", response_class=HTMLResponse)
async def read_users_items_read_jancode(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="users/readjancode.html",
        context={},
    )


@router.get("/add/jancode", response_class=HTMLResponse)
async def read_users_items_add_jancode(request: Request, jan_code: Optional[str] = None):
    context = AddItemFormResult(jan_code=jan_code).get_context()
    return templates.TemplateResponse(
        request=request,
        name="users/addjancode.html",
        context=context,
    )


@router.post("/add", response_class=HTMLResponse)
async def read_users_items_add(
    request: Request, addjancodeinfopostform: AddJanCodePostForm = Depends()
):
    result = await AddJanCodeForm(
        jancodeinfocreator=ConnectToAPIJanCodeInfoCreator(
            url=str(
                request.url_for(
                    "read_api_item_jancodeinfo",
                    jan_code=addjancodeinfopostform.jan_code,
                )
            ),
            factory=JanCodeInfoFactory(),
        ),
        addjancodepostform=addjancodeinfopostform,
        jancodefactory=JanCodeFactory(),
    ).execute()
    context = result.get_context()
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
