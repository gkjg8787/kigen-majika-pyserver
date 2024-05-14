from pydantic import BaseModel

from domain.models import IItemRepository, Item
from router.api.param import ItemRequestParam, ItemListRequestParam
from application.items import IItemQueryService, ItemQueryCommand


class ItemListResult(BaseModel):
    items: list[Item] = []
    error_msg: str = ""


class ItemList:
    itemqueryservice: IItemQueryService

    def __init__(self, itemqueryservice: IItemQueryService):
        self.itemqueryservice = itemqueryservice

    async def get(self, itemlistrequestparam: ItemListRequestParam) -> ItemListResult:
        command = ItemQueryCommand(**itemlistrequestparam.model_dump())
        result = await self.itemqueryservice.find_all(itemquerycommand=command)
        return ItemListResult(items=result.items)


class ItemOne:
    itemrepository: IItemRepository

    def __init__(self, repository: IItemRepository):
        self.itemrepository = repository

    async def get(self, itemrequestparam: ItemRequestParam) -> ItemListResult:
        item = await self.itemrepository.find_by_id(id=itemrequestparam.id)
        if not item:
            return ItemListResult()
        return ItemListResult(items=[item])
