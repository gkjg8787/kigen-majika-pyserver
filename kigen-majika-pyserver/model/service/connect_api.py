from datetime import datetime, timezone

import httpx

from model.service import IJanCodeInfoCreator
from model.domain import JanCodeInfo, JanCodeInfoFactory
from router.usecase import JanCodeInfoResult


class ConnectToAPIJanCodeInfoCreator(IJanCodeInfoCreator):
    url: str

    def __init__(self, url: str):
        self.url = url

    async def create(self, jan_code: str) -> JanCodeInfo:
        async with httpx.AsyncClient() as client:
            res = await client.get(self.url)
            jancodeinforesult = JanCodeInfoResult(**res.json())
            if jancodeinforesult.jancodeinfo:
                return jancodeinforesult.jancodeinfo
            return JanCodeInfoFactory.create(
                jan_code=jan_code,
                name="",
                category="",
                manufacturer="",
                updated_at=datetime.now(timezone.utc),
            )
