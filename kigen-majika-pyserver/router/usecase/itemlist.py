from pydantic import BaseModel

from model.service import IItemRepository
from model.domain import Item
from router.param import ItemRequestParam


class ItemListResult(BaseModel):
    items: list[Item] = []
    error_msg: str = ""


class ItemList:
    itemrepository: IItemRepository

    def __init__(self, repository: IItemRepository):
        self.itemrepository = repository

    async def get_all(self) -> ItemListResult:
        items = await self.itemrepository.find_all()
        return ItemListResult(items=items)

    async def get_one(self, itemrequestparam: ItemRequestParam) -> ItemListResult:
        item = await self.itemrepository.find_by_id(id=itemrequestparam.id)
        if not item:
            return ItemListResult()
        return ItemListResult(items=[item])
