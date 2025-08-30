from datetime import datetime, tzinfo
import json

import httpx

from .shared import htmlcontext, htmlname, util as sutil
from .shared.readitemform import (
    GetOneItemForm,
    GetOneItemCommand,
)
from router.api.usecase import ItemDeleteResult
from router.html.param import DeleteItemPostForm, DeleteItemBulkPostForm


class DeleteItemFormResult(htmlcontext.HtmlContext):
    POST_ID: str = htmlname.POSTNAME.ID.value
    PARAM_ID: str = htmlname.POSTNAME.ID.value

    is_next_page: bool = False
    error_msg: str = ""
    id: int
    jan_code: str = ""
    name: str = ""
    inventory: int = 0
    place: str = ""
    category: str = ""
    manufacturer: str = ""
    text: str = ""
    expiry_date: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class DeleteItemInitForm:
    deleteitempostform: DeleteItemPostForm
    detail_api_url: str
    local_timezone: tzinfo

    def __init__(
        self,
        deleteitempostform: DeleteItemPostForm,
        detail_api_url: str,
        local_timezone: tzinfo,
    ):
        self.deleteitempostform = deleteitempostform
        self.detail_api_url = detail_api_url
        self.local_timezone = local_timezone

    async def execute(self) -> DeleteItemFormResult:
        getoneresult = await GetOneItemForm(
            command=GetOneItemCommand(id=self.deleteitempostform.id),
            detail_api_url=self.detail_api_url,
        ).execute()
        if getoneresult.error_msg:
            return DeleteItemFormResult(
                id=self.deleteitempostform.id, error_msg=getoneresult.error_msg
            )
        result = DeleteItemFormResult(
            **getoneresult.item.model_dump(exclude={"jan_code"}),
            jan_code=getoneresult.item.jan_code.value
        )
        if result.expiry_date:
            result.expiry_date = sutil.utcTolocaltime(
                result.expiry_date, tz=self.local_timezone
            ).date()
        result.created_at = sutil.utcTolocaltime(
            input_date=result.created_at, tz=self.local_timezone
        )
        result.updated_at = sutil.utcTolocaltime(
            input_date=result.updated_at, tz=self.local_timezone
        )
        return result


class DeleteItemBulkForm:
    deleteitembulkpostform: DeleteItemBulkPostForm
    delete_api_url: str

    def __init__(
        self,
        deleteitembulkpostform: DeleteItemBulkPostForm,
        delete_api_url: str,
    ):
        self.deleteitembulkpostform = deleteitembulkpostform
        self.delete_api_url = delete_api_url

    async def execute(self) -> None:
        async with httpx.AsyncClient() as client:
            request_body = {"ids": self.deleteitembulkpostform.delete_item_ids}
            res = await client.post(
                self.delete_api_url,
                json=request_body,
            )
            res.raise_for_status()


class DeleteItemForm:
    deleteitempostform: DeleteItemPostForm
    delete_api_url: str
    local_timezone: tzinfo

    def __init__(
        self,
        deleteitempostform: DeleteItemPostForm,
        delete_api_url: str,
        local_timezone: tzinfo,
    ):
        self.deleteitempostform = deleteitempostform
        self.delete_api_url = delete_api_url
        self.local_timezone = local_timezone

    async def execute(self) -> DeleteItemFormResult:
        async with httpx.AsyncClient() as client:
            res = await client.post(
                self.delete_api_url,
                json=json.loads(self.deleteitempostform.model_dump_json()),
            )
        result = DeleteItemFormResult(id=self.deleteitempostform.id, is_next_page=True)
        if not res.json():
            result.error_msg = "No Data"
            return result
        itemdeleteresult = ItemDeleteResult(**res.json())
        result = DeleteItemFormResult(
            **itemdeleteresult.model_dump(),
            id=self.deleteitempostform.id,
            name=self.deleteitempostform.name,
            is_next_page=True
        )
        if result.expiry_date:
            result.expiry_date = sutil.utcTolocaltime(
                result.expiry_date, tz=self.local_timezone
            ).date()
        result.created_at = sutil.utcTolocaltime(
            input_date=result.created_at, tz=self.local_timezone
        )
        result.updated_at = sutil.utcTolocaltime(
            input_date=result.updated_at, tz=self.local_timezone
        )
        return result
