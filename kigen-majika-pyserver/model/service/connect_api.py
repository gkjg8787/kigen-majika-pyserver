from ..domain import Item
import httpx

from model.service import IJanCodeInfoCreator
from model.service.jancode_item import JanCodeInfo
from router.usecase import ItemNameResult


class ConnectToAPIJanCodeInfoCreator(IJanCodeInfoCreator):
    url: str

    def __init__(self, url: str):
        self.url = url

    async def create(self, jan_code: str) -> JanCodeInfo:
        async with httpx.AsyncClient() as client:
            res = await client.get(self.url)
            inr = ItemNameResult(**res.json())
            if inr.name is None:
                inr.name = ""
            return JanCodeInfo(jan_code=jan_code, name=inr.name)
