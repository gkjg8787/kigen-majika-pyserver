from datetime import datetime, timezone

from pydantic import BaseModel

from model.service import IItemRepository
from model.domain import Item
from router.param import ItemDeleteParam


class ItemDeleteResult(BaseModel):
    error_msg: str = ""


class ItemDelete:
    itemrepository: IItemRepository

    def __init__(self, itemrepository: IItemRepository):
        self.itemrepository = itemrepository

    async def delete(self, itemdeleteparam: ItemDeleteParam) -> ItemDeleteResult:
        await self.itemrepository.delete_by_id(id=itemdeleteparam.id)
        return ItemDeleteResult()
