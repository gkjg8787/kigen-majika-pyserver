from abc import ABCMeta, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from model.domain import (
    Item,
    ItemNameData,
    ItemFactory,
    ItemCategoryData,
    ItemManufacturerData,
)
from model.database import (
    ItemInventory,
    ItemCategory,
    ItemName,
    ItemMemo,
    ItemManufacturer,
)
from .dbconvert import ItemToDBObject, DBToItem
from .dbdata_compare import (
    ItemInventoryDataCompare,
    ItemCategoryDataCompare,
    ItemNameDataCompare,
    ItemMemoDataCompare,
    ItemManufacturerDataCompare,
)


class IItemRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, item: Item):
        pass

    @abstractmethod
    async def find_by_jan_code(self, jan_code: str) -> list[Item]:
        pass

    @abstractmethod
    async def find_by_id(self, id: int) -> Item | None:
        pass

    @abstractmethod
    async def find_all(self) -> list[Item]:
        pass

    @abstractmethod
    async def delete_by_id(self, id: int) -> None:
        pass


class IItemNameRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, itemnamedata: ItemNameData):
        pass

    @abstractmethod
    async def find_by_jan_code(self, jan_code: str) -> ItemName | None:
        pass


class IItemCategoryRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, itemcategorydata: ItemCategoryData):
        pass

    @abstractmethod
    async def find_by_jan_code(self, jan_code: str) -> ItemCategory | None:
        pass


class IItemManufacturerRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, itemmanufacturerdata: ItemManufacturerData):
        pass

    @abstractmethod
    async def find_by_jan_code(self, jan_code: str) -> ItemManufacturer | None:
        pass


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
            select(ItemInventory, ItemName, ItemCategory, ItemMemo)
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
            select(ItemInventory, ItemName, ItemCategory, ItemMemo)
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


class ItemNameRepository(IItemNameRepository):
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, itemnamedata: ItemNameData):
        db = self.session
        iname: ItemName = await db.get(ItemName, itemnamedata.jan_code)
        new_iname = ItemName(jan_code=itemnamedata.jan_code, name=itemnamedata.name)
        if not iname:
            db.add(new_iname)
            await db.commit()
            await db.refresh(new_iname)
        elif not ItemNameDataCompare.equal(iname, new_iname):
            iname.name = new_iname.name
            iname.updated_at = new_iname.updated_at
            await db.commit()
            await db.refresh(iname)

    async def find_by_jan_code(self, jan_code: str) -> ItemName | None:
        db = self.session
        iname: ItemName = await db.get(ItemName, jan_code)
        if not iname:
            return None
        return iname


class ItemCategoryRepository(IItemCategoryRepository):
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, itemcategorydata: ItemCategoryData):
        db = self.session
        icate: ItemCategory = await db.get(ItemCategory, itemcategorydata.jan_code)
        new_icate = ItemCategory(
            jan_code=itemcategorydata.jan_code, category=itemcategorydata.category
        )
        if not icate:
            db.add(new_icate)
            await db.commit()
            await db.refresh(new_icate)
        elif not ItemCategoryDataCompare.equal(icate, new_icate):
            icate.category = new_icate.category
            icate.updated_at = new_icate.updated_at
            await db.commit()
            await db.refresh(icate)

    async def find_by_jan_code(self, jan_code: str) -> ItemCategory | None:
        db = self.session
        icate: ItemCategory = await db.get(ItemCategory, jan_code)
        if not icate:
            return None
        return icate


class ItemManufacturerRepository(IItemManufacturerRepository):
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, itemmanufacturerdata: ItemManufacturerData):
        db = self.session
        imanu: ItemManufacturer = await db.get(
            ItemManufacturer, itemmanufacturerdata.jan_code
        )
        new_imanu = ItemManufacturer(
            jan_code=itemmanufacturerdata.jan_code,
            manufacturer=itemmanufacturerdata.manufacturer,
        )
        if not imanu:
            db.add(new_imanu)
            await db.commit()
            await db.refresh(new_imanu)
        elif not ItemManufacturerDataCompare.equal(imanu, new_imanu):
            imanu.manufacturer = new_imanu.manufacturer
            imanu.updated_at = new_imanu.updated_at
            await db.commit()
            await db.refresh(imanu)

    async def find_by_jan_code(self, jan_code: str) -> ItemManufacturer | None:
        db = self.session
        imanu: ItemManufacturer = await db.get(ItemManufacturer, jan_code)
        if not imanu:
            return None
        return imanu


class ItemDictRepository(IItemRepository):
    database: dict[int, Item]

    def __init__(self, data: dict):
        self.database = data

    async def save(self, item: Item):
        self.database[item.id] = item

    async def find_by_jan_code(self, jan_code: str) -> list[Item]:
        results: list[Item] = []
        for v in self.database.values():
            if v.jan_code == jan_code:
                results.append(v)
        return results

    async def find_by_id(self, id: int) -> Item | None:
        return self.database.get(id, None)

    async def find_all(self) -> list[Item]:
        return list(self.database.values())

    async def delete_by_id(self, id: int) -> None:
        if id not in self.database:
            return None
        item = self.database.pop(id)
        return


class ItemNameDictRepository(IItemNameRepository):
    database: dict[str, ItemName]

    def __init__(self, data: dict):
        self.database = data

    async def save(self, itemnamedata: ItemNameData):
        self.database[itemnamedata.jan_code] = ItemName(
            jan_code=itemnamedata.jan_code, name=itemnamedata.name
        )

    async def find_by_jan_code(self, jan_code: str) -> ItemName | None:
        return self.database.get(jan_code, None)


class ItemCategoryDictRepository(IItemCategoryRepository):
    database: dict[str, ItemCategory]

    def __init__(self, data: dict):
        self.database = data

    async def save(self, itemcategorydata: ItemCategoryData):
        self.database[itemcategorydata.jan_code] = ItemCategory(
            jan_code=itemcategorydata.jan_code, category=itemcategorydata.category
        )

    async def find_by_jan_code(self, jan_code: str) -> ItemCategory | None:
        return self.database.get(jan_code, None)


class ItemManufacturerDictRepository(IItemManufacturerRepository):
    database: dict[str, ItemManufacturer]

    def __init__(self, data: dict):
        self.database = data

    async def save(self, itemmanufacturerdata: ItemManufacturerData):
        self.database[itemmanufacturerdata.jan_code] = ItemManufacturer(
            jan_code=itemmanufacturerdata.jan_code,
            manufacturer=itemmanufacturerdata.manufacturer,
        )

    async def find_by_jan_code(self, jan_code: str) -> ItemManufacturer | None:
        return self.database.get(jan_code, None)
