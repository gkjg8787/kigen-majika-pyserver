from datetime import datetime, timezone

import httpx

from .jancode_item import IJanCodeInfoCreator
from domain.models import JanCodeInfo, IJanCodeInfoFactory, JanCode
from router.api.usecase import JanCodeInfoResult


class ConnectToAPIJanCodeInfoCreator(IJanCodeInfoCreator):
    url: str
    jancodeinfofactory: IJanCodeInfoFactory

    def __init__(self, url: str, factory: IJanCodeInfoFactory):
        self.url = url
        self.jancodeinfofactory = factory

    async def create(self, jan_code: JanCode) -> JanCodeInfo:
        async with httpx.AsyncClient() as client:
            res = await client.get(self.url)
            jancodeinforesult = JanCodeInfoResult(**res.json())
            if jancodeinforesult.jancodeinfo:
                return jancodeinforesult.jancodeinfo
            return self.jancodeinfofactory.create(
                jan_code=jan_code,
                name="",
                category="",
                manufacturer="",
                updated_at=datetime.now(timezone.utc),
            )
