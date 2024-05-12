from datetime import datetime, timezone

from pydantic import BaseModel

from model.service import IItemRepository, IItemIdentity, IJanCodeInfoRepository
from model.domain import IItemFactory, Item
from router.param import ItemCreateParam


class ItemCreateResult(BaseModel):
    item: Item | None = None
    error_msg: str = ""


class ItemCreate:
    itemrepository: IItemRepository
    itemidentity: IItemIdentity
    itemfactory: IItemFactory
    jancodeinforepository: IJanCodeInfoRepository

    def __init__(
        self,
        itemrepository: IItemRepository,
        itemidentity: IItemIdentity,
        itemfactory: IItemFactory,
        jancodeinforepository: IJanCodeInfoRepository,
    ):
        self.itemrepository = itemrepository
        self.itemidentity = itemidentity
        self.itemfactory = itemfactory
        self.jancodeinforepository = jancodeinforepository

    async def create(self, itemcreateparam: ItemCreateParam) -> ItemCreateResult:
        result = ItemCreateResult()
        nextid_str = await self.itemidentity.next_identity()
        if not nextid_str:
            result.error_msg = "failed to get identity"
            return result
        itemcreateparam = await self.fill_in_missing_info(
            itemcreateparam=itemcreateparam
        )
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

    def is_get_jancodeinfo(self, itemcreateparam: ItemCreateParam) -> bool:
        if (
            not itemcreateparam.name
            or not itemcreateparam.category
            or not itemcreateparam.manufacturer
        ):
            return True

    async def fill_in_missing_info(
        self, itemcreateparam: ItemCreateParam
    ) -> ItemCreateParam:
        if not self.is_get_jancodeinfo(itemcreateparam=itemcreateparam):
            return itemcreateparam
        jancodeinfo = await self.jancodeinforepository.find_by_jan_code(
            jan_code=itemcreateparam.jan_code
        )
        result = ItemCreateParam(**itemcreateparam.model_dump())
        if not jancodeinfo:
            return result
        if jancodeinfo.name and not itemcreateparam.name:
            result.name = jancodeinfo.name
        if jancodeinfo.category and not itemcreateparam.category:
            result.category = jancodeinfo.category
        if jancodeinfo.manufacturer and not itemcreateparam.manufacturer:
            result.manufacturer = jancodeinfo.manufacturer
        return result
