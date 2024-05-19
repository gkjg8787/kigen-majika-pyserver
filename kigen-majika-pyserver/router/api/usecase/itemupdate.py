from datetime import datetime, timezone

from pydantic import BaseModel

from domain.models import IItemRepository, Item, IItemFactory, IJanCodeFactory
from router.api.param import ItemUpdateParam, ItemUpdateParamToDomain, ItemToParam


class ItemUpdateResult(BaseModel):
    item: Item | None = None
    is_update: bool
    error_msg: str = ""


class ItemUpdate:
    itemrepository: IItemRepository
    itemfactory: IItemFactory
    jancodefactory: IJanCodeFactory

    def __init__(
        self,
        itemrepository: IItemRepository,
        itemfactory: IItemFactory,
        jancodefactory: IJanCodeFactory,
    ):
        self.itemrepository = itemrepository
        self.itemfactory = itemfactory
        self.jancodefactory = jancodefactory

    async def update(self, itemupdateparam: ItemUpdateParam) -> ItemUpdateResult:
        item = await self.itemrepository.find_by_id(itemupdateparam.id)
        if not item:
            return ItemUpdateResult(
                is_update=False, error_msg=f"Not Found Data id={itemupdateparam.id}"
            )
        if self.toItemUpdateParam(item=item) == itemupdateparam:
            return ItemUpdateResult(is_update=False, error_msg=f"no update parameter")
        new_item = self.toItem(
            itemupdateparam=itemupdateparam,
            created_at=item.created_at,
            updated_at=datetime.now(timezone.utc),
        )
        await self.itemrepository.save(new_item)
        return ItemUpdateResult(item=new_item, is_update=True)

    def toItemUpdateParam(self, item: Item) -> ItemUpdateParam:
        return ItemToParam().toItemUpdateParam(item=item)

    def toItem(
        self,
        itemupdateparam: ItemUpdateParam,
        created_at: datetime,
        updated_at: datetime,
    ) -> Item:
        return ItemUpdateParamToDomain(
            itemfactory=self.itemfactory, jancodefactory=self.jancodefactory
        ).toItem(
            itemupdateparam=itemupdateparam,
            created_at=created_at,
            updated_at=updated_at,
        )
