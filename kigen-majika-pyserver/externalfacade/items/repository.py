from abc import ABCMeta, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from domain.models import (
    Item,
    JanCodeInfo,
    IItemRepository,
    IJanCodeInfoRepository,
)
from .items import (
    ItemInventory,
    ItemCategory,
    ItemName,
    ItemMemo,
    ItemManufacturer,
)
from .factory import ItemFactory, JanCodeInfoFactory
from .dbconvert import ItemToDBObject, DBToItem, JanCodeInfoToDBObject, DBToJanCodeInfo
from .dbdata_compare import (
    ItemInventoryDataCompare,
    ItemCategoryDataCompare,
    ItemNameDataCompare,
    ItemMemoDataCompare,
    ItemManufacturerDataCompare,
)


class ItemRepository(IItemRepository):
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, item: Item):
        db = self.session
        iinv: ItemInventory = await db.get(ItemInventory, item.id)
        new_iinv = ItemToDBObject.toItemInventory(item)
        if not iinv:
            db.add(new_iinv)
            await db.commit()
            await db.refresh(new_iinv)
        elif not ItemInventoryDataCompare.equal(iinv, new_iinv):
            iinv.inventory = new_iinv.inventory
            iinv.place = new_iinv.place
            iinv.updated_at = new_iinv.updated_at
            iinv.expiry_date = new_iinv.expiry_date
            await db.commit()
            await db.refresh(iinv)

        iname: ItemName = await db.get(ItemName, item.jan_code)
        new_iname = ItemToDBObject.toItemName(item)
        if not iname:
            db.add(new_iname)
            await db.commit()
            await db.refresh(new_iname)
        elif not ItemNameDataCompare.equal(iname, new_iname):
            iname.name = new_iname.name
            iname.updated_at = new_iname.updated_at
            await db.commit()
            await db.refresh(iname)

        icate: ItemCategory = await db.get(ItemCategory, item.jan_code)
        new_icate = ItemToDBObject.toItemCategory(item)
        if not icate:
            db.add(new_icate)
            await db.commit()
            await db.refresh(new_icate)
        elif not ItemCategoryDataCompare.equal(icate, new_icate):
            icate.category = new_icate.category
            icate.updated_at = new_icate.updated_at
            await db.commit()
            await db.refresh(icate)

        imanu: ItemManufacturer = await db.get(ItemManufacturer, item.jan_code)
        new_imanu = ItemToDBObject.toItemManufacturer(item)
        if not imanu:
            db.add(new_imanu)
            await db.commit()
            await db.refresh(new_imanu)
        elif not ItemManufacturerDataCompare.equal(imanu, new_imanu):
            imanu.manufacturer = new_imanu.manufacturer
            imanu.updated_at = new_imanu.updated_at
            await db.commit()
            await db.refresh(imanu)

        imemo: ItemMemo = await db.get(ItemMemo, item.id)
        new_imemo = ItemToDBObject.toItemMemo(item)
        if not imemo:
            db.add(new_imemo)
            await db.commit()
            await db.refresh(new_imemo)
        elif not ItemMemoDataCompare.equal(imemo, new_imemo):
            imemo.text = new_imemo.text
            imemo.updated_at = new_imemo.updated_at
            await db.commit()
            await db.refresh(imemo)

    @classmethod
    def _to_items(cls, select_results):
        dbtoitem = DBToItem(ItemFactory())
        results: list[Item] = []
        for r in select_results:
            item = dbtoitem.toItem(
                item_inventory=r[ItemInventory.__name__],
                item_name=r[ItemName.__name__],
                item_category=r[ItemCategory.__name__],
                item_manufacturer=r[ItemManufacturer.__name__],
                item_memo=r[ItemMemo.__name__],
            )
            results.append(item)
        return results

    async def find_by_jan_code(self, jan_code: str) -> list[Item]:
        db = self.session
        stmt = (
            select(ItemInventory, ItemName, ItemCategory, ItemManufacturer, ItemMemo)
            .select_from(ItemInventory)
            .join(ItemName, ItemInventory.jan_code == ItemName.jan_code)
            .join(ItemCategory, ItemInventory.jan_code == ItemCategory.jan_code)
            .join(ItemManufacturer, ItemInventory.jan_code == ItemManufacturer.jan_code)
            .join(ItemMemo, ItemInventory.id == ItemMemo.id)
            .where(ItemInventory.jan_code == jan_code)
            .order_by(ItemInventory.id.asc())
        )
        ret = await db.execute(stmt)
        return self._to_items(ret.mappings().all())

    async def _find_by_id(self, id: int, db: AsyncSession) -> Item | None:
        stmt = (
            select(ItemInventory, ItemName, ItemCategory, ItemManufacturer, ItemMemo)
            .select_from(ItemInventory)
            .join(ItemName, ItemInventory.jan_code == ItemName.jan_code)
            .join(ItemCategory, ItemInventory.jan_code == ItemCategory.jan_code)
            .join(ItemManufacturer, ItemInventory.jan_code == ItemManufacturer.jan_code)
            .join(ItemMemo, ItemInventory.id == ItemMemo.id)
            .where(ItemInventory.id == id)
        )
        return await db.execute(stmt)

    async def find_by_id(self, id: int) -> Item | None:
        db = self.session
        ret = await self._find_by_id(id=id, db=db)
        items = self._to_items(ret.mappings().all())
        if items:
            return items[0]
        return None

    async def find_all(self) -> list[Item]:
        db = self.session
        stmt = (
            select(ItemInventory, ItemName, ItemCategory, ItemManufacturer, ItemMemo)
            .select_from(ItemInventory)
            .join(ItemName, ItemInventory.jan_code == ItemName.jan_code)
            .join(ItemCategory, ItemInventory.jan_code == ItemCategory.jan_code)
            .join(ItemManufacturer, ItemInventory.jan_code == ItemManufacturer.jan_code)
            .join(ItemMemo, ItemInventory.id == ItemMemo.id)
            .order_by(ItemInventory.id.asc())
        )
        ret = await db.execute(stmt)
        return self._to_items(ret.mappings().all())

    async def delete_by_id(self, id: int) -> None:
        db = self.session
        ret = await self._find_by_id(id=id, db=db)
        ret_objs = ret.mappings().all()
        if not ret_objs:
            return None
        ret_obj = ret_objs[0]
        await db.delete(ret_obj[ItemMemo.__name__])
        await db.delete(ret_obj[ItemInventory.__name__])
        await db.commit()


class JanCodeInfoRepository(IJanCodeInfoRepository):
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, jancodeinfo: JanCodeInfo):
        db = self.session
        iname: ItemName = await db.get(ItemName, jancodeinfo.jan_code)
        new_iname = JanCodeInfoToDBObject.toItemName(jancodeinfo)
        if not iname:
            db.add(new_iname)
            await db.commit()
            await db.refresh(new_iname)
        elif not ItemNameDataCompare.equal(iname, new_iname):
            iname.name = new_iname.name
            iname.updated_at = new_iname.updated_at
            await db.commit()
            await db.refresh(iname)

        icate: ItemCategory = await db.get(ItemCategory, jancodeinfo.jan_code)
        new_icate = JanCodeInfoToDBObject.toItemCategory(jancodeinfo)
        if not icate:
            db.add(new_icate)
            await db.commit()
            await db.refresh(new_icate)
        elif not ItemCategoryDataCompare.equal(icate, new_icate):
            icate.category = new_icate.category
            icate.updated_at = new_icate.updated_at
            await db.commit()
            await db.refresh(icate)

        imanu: ItemManufacturer = await db.get(ItemManufacturer, jancodeinfo.jan_code)
        new_imanu = JanCodeInfoToDBObject.toItemManufacturer(jancodeinfo)
        if not imanu:
            db.add(new_imanu)
            await db.commit()
            await db.refresh(new_imanu)
        elif not ItemManufacturerDataCompare.equal(imanu, new_imanu):
            imanu.manufacturer = new_imanu.manufacturer
            imanu.updated_at = new_imanu.updated_at
            await db.commit()
            await db.refresh(imanu)

    async def find_by_jan_code(self, jan_code: str) -> JanCodeInfo | None:
        db = self.session
        stmt = (
            select(ItemName, ItemCategory, ItemManufacturer)
            .select_from(ItemName)
            .join(ItemCategory, ItemName.jan_code == ItemCategory.jan_code)
            .join(ItemManufacturer, ItemName.jan_code == ItemManufacturer.jan_code)
            .where(ItemName.jan_code == jan_code)
        )
        ret = await db.execute(stmt)
        one = ret.mappings().one_or_none()
        if not one:
            return None
        jancodeinfo = DBToJanCodeInfo(JanCodeInfoFactory()).toJanCodeInfo(
            item_name=one[ItemName.__name__],
            item_category=one[ItemCategory.__name__],
            item_manufacturer=one[ItemManufacturer.__name__],
        )
        return jancodeinfo
