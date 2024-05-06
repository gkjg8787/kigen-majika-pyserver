import httpx

from datetime import tzinfo

from model.domain import Item
from router.usecase.shared import htmlcontext, util as sutil
from router.usecase.shared import htmlname


class ItemListInHTMLResult(htmlcontext.HtmlContext):
    items: list[Item] = []
    items_length: int = 0
    error_msg: str = ""
    PARAM_ID: str = htmlname.POSTNAME.ID.value


class ItemListInHTML:
    api_url: str
    local_timezone: tzinfo

    def __init__(self, api_url: str, local_timezone: tzinfo):
        self.api_url = api_url
        self.local_timezone = local_timezone

    async def execute(self) -> ItemListInHTMLResult:
        async with httpx.AsyncClient() as client:
            res = await client.get(self.api_url)
        if not res.json():
            return ItemListInHTMLResult()
        result = ItemListInHTMLResult(**res.json())
        if result.items:
            result.items_length = len(result.items)
            for i in result.items:
                self.toLocaltimezone(item=i, tz=self.local_timezone)
        return result

    def toLocaltimezone(self, item: Item, tz: tzinfo) -> None:
        if item.expiry_date:
            item.expiry_date = sutil.utcTolocaltime(input_date=item.expiry_date, tz=tz)
        item.created_at = sutil.utcTolocaltime(input_date=item.created_at, tz=tz)
        item.updated_at = sutil.utcTolocaltime(input_date=item.updated_at, tz=tz)
