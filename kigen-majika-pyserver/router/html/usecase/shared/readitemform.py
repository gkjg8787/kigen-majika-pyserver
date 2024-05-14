import json

import httpx

from pydantic import BaseModel

from router.api.usecase import ItemListResult
from domain.models import Item


class GetOneItemResult(BaseModel):
    item: Item | None = None
    error_msg: str = ""


class GetOneItemCommand(BaseModel):
    id: int


class GetOneItemForm:
    command: GetOneItemCommand
    detail_api_url: str

    def __init__(self, command: GetOneItemCommand, detail_api_url: str):
        self.command = command
        self.detail_api_url = detail_api_url

    async def execute(self) -> GetOneItemResult:
        async with httpx.AsyncClient() as client:
            res = await client.post(
                self.detail_api_url,
                json=json.loads(self.command.model_dump_json()),
            )
        if not res.json():
            return GetOneItemResult(error_msg="Not Found Data")
        itemlistres = ItemListResult(**res.json())
        if not itemlistres.items:
            return GetOneItemResult(error_msg="Not Found Item")
        return GetOneItemResult(item=itemlistres.items[0])
