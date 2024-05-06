from datetime import datetime
import json

import httpx

from router.usecase.shared import htmlcontext, htmlname
from router.usecase import ItemCreateResult
from router.param import AddItemPostForm
from model.service import IJanCodeInfoCreator


class AddItemFormResult(htmlcontext.HtmlContext):
    POST_JAN_CODE: str = htmlname.POSTNAME.JAN_CODE.value
    POST_NAME: str = htmlname.POSTNAME.NAME.value
    POST_INVENTORY: str = htmlname.POSTNAME.INVENTORY.value
    POST_CATEGORY: str = htmlname.POSTNAME.CATEGORY.value
    POST_MANUFACTURER: str = htmlname.POSTNAME.MANUFACTURER.value
    POST_TEXT: str = htmlname.POSTNAME.TEXT.value
    POST_EXPIRY_DATE: str = htmlname.POSTNAME.EXPIRY_DATE.value
    POST_TIMEZONE: str = htmlname.POSTNAME.LOCAL_TIMEZONE.value

    is_next_page: bool = False
    error_msg: str = ""
    jan_code: str = ""
    name: str = ""
    inventory: int = 0
    place: str = ""
    category: str = ""
    manufacturer: str = ""
    text: str = ""
    expiry_date: datetime | None = None
    local_timezone: str = htmlname.LocalTimeZone.JST


class AddItemForm:
    jancodeinfocreator: IJanCodeInfoCreator
    additempostform: AddItemPostForm
    create_url: str

    def __init__(
        self,
        jancodeinfocreator: IJanCodeInfoCreator,
        additempostform: AddItemPostForm,
        create_url: str,
    ):
        self.additempostform = additempostform
        self.jancodeinfocreator = jancodeinfocreator
        self.create_url = create_url

    async def execute(self) -> AddItemFormResult:
        additempostform: AddItemPostForm = self.additempostform
        if not additempostform.name:
            res = await self.jancodeinfocreator.create(
                jan_code=additempostform.jan_code
            )
            additempostform.name = res.name
        result = await self.connect_to_create_api(
            url=self.create_url, additempostform=additempostform
        )
        return result

    async def connect_to_create_api(
        self, url: str, additempostform: AddItemPostForm
    ) -> AddItemFormResult:
        async with httpx.AsyncClient() as client:
            res = await client.post(
                url,
                json=json.loads(additempostform.model_dump_json()),
            )
            icr = ItemCreateResult(**res.json())

            if not icr.item:
                if not icr.error_msg:
                    return AddItemFormResult(
                        is_next_page=True,
                        jan_code=additempostform.jan_code,
                        error_msg="Fail Create Item",
                    )
                else:
                    return AddItemFormResult(
                        is_next_page=True,
                        jan_code=additempostform.jan_code,
                        error_msg=icr.error_msg,
                    )
            return AddItemFormResult(is_next_page=True, **icr.item.model_dump())
