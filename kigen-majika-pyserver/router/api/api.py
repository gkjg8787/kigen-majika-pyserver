from fastapi import APIRouter, Request, Form, Depends, status, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse

from sqlalchemy.ext.asyncio import AsyncSession

from externalfacade import get_async_session
from externalfacade.items import (
    ItemRepository,
    ItemQueryService,
    JanCodeInfoRepository,
    ItemIdentity,
    ItemFactory,
    JanCodeInfoFactory,
)
from application.items import OnlineJanCodeInfoCreator
from .usecase import (
    GetOnlineJanCodeInfo,
    ItemList,
    ItemOne,
    ItemCreate,
    ItemUpdate,
    ItemDelete,
    ItemListResult,
    JanCodeInfoResult,
    ItemCreateResult,
    ItemUpdateResult,
    ItemDeleteResult,
)
from .param import (
    ItemListRequestParam,
    ItemUpdateParam,
    ItemCreateParam,
    ItemDeleteParam,
    ItemRequestParam,
)

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


@router.get("/items/{jan_code}/info", response_model=JanCodeInfoResult)
async def read_api_item_jancodeinfo(
    request: Request,
    jan_code: str,
    db: AsyncSession = Depends(get_async_session),
):
    results = await GetOnlineJanCodeInfo(
        repository=JanCodeInfoRepository(db),
        jancodeinfocreator=OnlineJanCodeInfoCreator(factory=JanCodeInfoFactory()),
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
        jancodeinforepository=JanCodeInfoRepository(db),
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
