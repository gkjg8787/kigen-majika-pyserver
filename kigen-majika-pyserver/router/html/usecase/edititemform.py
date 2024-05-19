from datetime import datetime, tzinfo
import json

import httpx

from .shared import htmlcontext, htmlname, util as sutil
from .shared.readitemform import GetOneItemCommand, GetOneItemForm
from router.api.usecase import ItemUpdateResult
from router.html.param import EditItemGetForm, EditItemPostForm


class EditItemFormResult(htmlcontext.HtmlContext):
    POST_ID: str = htmlname.POSTNAME.ID.value
    POST_JAN_CODE: str = htmlname.POSTNAME.JAN_CODE.value
    POST_NAME: str = htmlname.POSTNAME.NAME.value
    POST_INVENTORY: str = htmlname.POSTNAME.INVENTORY.value
    POST_PLACE: str = htmlname.POSTNAME.PLACE.value
    POST_CATEGORY: str = htmlname.POSTNAME.CATEGORY.value
    POST_MANUFACTURER: str = htmlname.POSTNAME.MANUFACTURER.value
    POST_TEXT: str = htmlname.POSTNAME.TEXT.value
    POST_EXPIRY_DATE: str = htmlname.POSTNAME.EXPIRY_DATE.value
    POST_TIMEZONE: str = htmlname.POSTNAME.LOCAL_TIMEZONE.value

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
    local_timezone: str = htmlname.LocalTimeZone.JST


class EditItemInitForm:
    edititemgetform: EditItemGetForm
    detail_api_url: str
    local_timezone: tzinfo

    def __init__(
        self,
        edititemgetform: EditItemGetForm,
        detail_api_url: str,
        local_timezone: tzinfo,
    ):
        self.edititemgetform = edititemgetform
        self.detail_api_url = detail_api_url
        self.local_timezone = local_timezone

    async def execute(self) -> EditItemFormResult:
        getoneresult = await GetOneItemForm(
            command=GetOneItemCommand(id=self.edititemgetform.id),
            detail_api_url=self.detail_api_url,
        ).execute()
        if getoneresult.error_msg:
            return EditItemFormResult(
                id=self.edititemgetform.id, error_msg=getoneresult.error_msg
            )
        result = EditItemFormResult(
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


class EditItemForm:
    edititempostform: EditItemPostForm
    detail_api_url: str
    update_api_url: str
    local_timezone: tzinfo

    def __init__(
        self,
        edititempostform: EditItemPostForm,
        detail_api_url: str,
        update_api_url: str,
        local_timezone: tzinfo,
    ):
        self.edititempostform = edititempostform
        self.detail_api_url = detail_api_url
        self.update_api_url = update_api_url
        self.local_timezone = local_timezone

    async def execute(self) -> EditItemFormResult:
        async with httpx.AsyncClient() as client:
            res = await client.post(
                self.update_api_url,
                json=json.loads(self.edititempostform.model_dump_json()),
            )
        result = EditItemFormResult(id=self.edititempostform.id, is_next_page=True)
        if not res.json():
            result.error_msg = "No Data"
            return result
        itemupdateresult = ItemUpdateResult(**res.json())
        if not itemupdateresult.is_update:
            result.error_msg = "No Update"
            return result
        result = EditItemFormResult(
            **itemupdateresult.item.model_dump(exclude={"jan_code"}),
            jan_code=itemupdateresult.item.jan_code.value,
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
