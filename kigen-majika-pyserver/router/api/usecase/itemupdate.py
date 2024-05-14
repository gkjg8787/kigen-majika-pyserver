from datetime import datetime, timezone

from pydantic import BaseModel

from domain.models import IItemRepository, Item, IItemFactory
from router.api.param import ItemUpdateParam


class ItemUpdateResult(BaseModel):
    item: Item | None = None
    is_update: bool
    error_msg: str = ""


class ItemUpdate:
    itemrepository: IItemRepository
    itemfactory: IItemFactory

    def __init__(self, itemrepository: IItemRepository, itemfactory: IItemFactory):
        self.itemrepository = itemrepository
        self.itemfactory = itemfactory

    async def update(self, itemupdateparam: ItemUpdateParam) -> ItemUpdateResult:
        item = await self.itemrepository.find_by_id(itemupdateparam.id)
        if not item:
            return ItemUpdateResult(
                is_update=False, error_msg=f"Not Found Data id={itemupdateparam.id}"
            )
        if ItemUpdateParam(**item.model_dump()) == itemupdateparam:
            return ItemUpdateResult(is_update=False, error_msg=f"no update parameter")
        new_item = self.itemfactory.create(
            **itemupdateparam.model_dump(),
            created_at=item.created_at,
            updated_at=datetime.now(timezone.utc),
        )
        await self.itemrepository.save(new_item)
        return ItemUpdateResult(item=new_item, is_update=True)
