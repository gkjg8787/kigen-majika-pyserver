from datetime import datetime

from domain.models import Item, IJanCodeFactory, IItemFactory
from .items import ItemUpdateParam


class ItemUpdateParamToDomain:
    jancodefactory: IJanCodeFactory
    itemfactory: IItemFactory

    def __init__(self, itemfactory: IItemFactory, jancodefactory: IJanCodeFactory):
        self.itemfactory = itemfactory
        self.jancodefactory = jancodefactory

    def toItem(
        self,
        itemupdateparam: ItemUpdateParam,
        created_at: datetime,
        updated_at: datetime,
    ) -> Item:
        return self.itemfactory.create(
            **itemupdateparam.model_dump(exclude={"jan_code"}),
            jan_code=self.jancodefactory.create(jan_code=itemupdateparam.jan_code),
            created_at=created_at,
            updated_at=updated_at,
        )


class ItemToParam:
    def toItemUpdateParam(self, item: Item) -> ItemUpdateParam:
        return ItemUpdateParam(
            **item.model_dump(exclude={"jan_code"}), jan_code=item.jan_code.value
        )
