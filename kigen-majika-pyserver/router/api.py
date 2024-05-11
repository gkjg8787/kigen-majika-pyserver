from fastapi import APIRouter, Request, Form, Depends, status, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse

from sqlalchemy.ext.asyncio import AsyncSession

from model.database import get_async_session
from router.usecase import (
    OnlineItemName,
    ItemList,
    ItemOne,
    ItemCreate,
    ItemUpdate,
    ItemDelete,
    ItemListResult,
    ItemNameResult,
    ItemCreateResult,
    ItemUpdateResult,
    ItemDeleteResult,
)
from router.param import (
    ItemListRequestParam,
    ItemUpdateParam,
    ItemCreateParam,
    ItemDeleteParam,
    ItemRequestParam,
)
from model.service import (
    ItemRepository,
    ItemQueryService,
    ItemNameRepository,
    OnlineJanCodeInfoCreator,
    ItemIdentity,
)
from model.domain import ItemFactory
import settings

router = APIRouter(prefix="/api", tags=["api"])


@router.post("/items", response_model=ItemListResult)
async def read_api_items(
    request: Request,
    itemlistrequestparam: ItemListRequestParam,
    db: AsyncSession = Depends(get_async_session),
):
    results = await ItemList(ItemQueryService(db)).get(
        itemlistrequestparam=itemlistrequestparam
    )
    return results


@router.post("/items/detail", response_model=ItemListResult)
async def read_api_item_detail(
    request: Request,
    itemrequestparam: ItemRequestParam,
    db: AsyncSession = Depends(get_async_session),
):
    results = await ItemOne(ItemRepository(db)).get(itemrequestparam=itemrequestparam)
    return results


@router.get("/items/{jan_code}/name", response_model=ItemNameResult)
async def read_api_itemname(
    request: Request,
    jan_code: str,
    db: AsyncSession = Depends(get_async_session),
):
    results = await OnlineItemName(
        repository=ItemNameRepository(db),
        jancodeinfocreator=OnlineJanCodeInfoCreator(),
        get_info_online=settings.GET_INFO_ONLINE,
    ).get_or_create(jan_code=jan_code)
    return results


@router.post("/items/create", response_model=ItemCreateResult)
async def read_api_item_create(
    request: Request,
    itemcreateparam: ItemCreateParam,
    db: AsyncSession = Depends(get_async_session),
):
    itemcreateresult = await ItemCreate(
        itemrepository=ItemRepository(db),
        itemidentity=ItemIdentity(db),
        itemfactory=ItemFactory(),
    ).create(itemcreateparam)
    return itemcreateresult


@router.post("/items/update", response_model=ItemUpdateResult)
async def read_api_item_update(
    request: Request,
    itemupdateparam: ItemUpdateParam,
    db: AsyncSession = Depends(get_async_session),
):
    itemuupdateresult = await ItemUpdate(
        itemrepository=ItemRepository(db), itemfactory=ItemFactory()
    ).update(itemupdateparam)
    return itemuupdateresult


@router.post("/items/delete", response_model=ItemDeleteResult)
async def read_api_item_delete(
    request: Request,
    itemdeleteparam: ItemDeleteParam,
    db: AsyncSession = Depends(get_async_session),
):
    itemdeleteresult = await ItemDelete(itemrepository=ItemRepository(db)).delete(
        itemdeleteparam=itemdeleteparam
    )
    return itemdeleteresult
