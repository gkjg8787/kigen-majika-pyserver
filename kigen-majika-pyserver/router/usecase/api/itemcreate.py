from datetime import datetime, timezone

from pydantic import BaseModel

from model.service import IItemRepository, IItemIdentity
from model.domain import IItemFactory, Item
from router.param import ItemCreateParam


class ItemCreateResult(BaseModel):
    item: Item | None = None
    error_msg: str = ""


class ItemCreate:
    itemrepository: IItemRepository
    itemidentity: IItemIdentity
    itemfactory: IItemFactory

    def __init__(
        self,
        itemrepository: IItemRepository,
        itemidentity: IItemIdentity,
        itemfactory: IItemFactory,
    ):
        self.itemrepository = itemrepository
        self.itemidentity = itemidentity
        self.itemfactory = itemfactory

    async def create(self, itemcreateparam: ItemCreateParam) -> ItemCreateResult:
        result = ItemCreateResult()
        nextid_str = await self.itemidentity.next_identity()
        if not nextid_str:
            result.error_msg = "failed to get identity"
            return result
        utc_datetime = datetime.now(timezone.utc)
        item = self.itemfactory.create(
            id=int(nextid_str),
            name=itemcreateparam.name,
            jan_code=itemcreateparam.jan_code,
            inventory=itemcreateparam.inventory,
            place=itemcreateparam.place,
            category=itemcreateparam.category,
            manufacturer=itemcreateparam.manufacturer,
            text=itemcreateparam.text,
            expiry_date=itemcreateparam.expiry_date,
            created_at=utc_datetime,
            updated_at=utc_datetime,
        )
        await self.itemrepository.save(item=item)
        result.item = item
        return result
