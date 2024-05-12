from model.database import (
    ItemInventory,
    ItemCategory,
    ItemMemo,
    ItemName,
    ItemManufacturer,
)
from model.domain import IItemFactory, Item, JanCodeInfo, IJanCodeInfoFactory


class ItemToDBObject:
    @classmethod
    def toItemInventory(cls, item: Item) -> ItemInventory:
        return ItemInventory(
            id=item.id,
            jan_code=item.jan_code,
            inventory=item.inventory,
            place=item.place,
            expiry_date=item.expiry_date,
            created_at=item.created_at,
            updated_at=item.updated_at,
        )

    @classmethod
    def toItemName(cls, item: Item) -> ItemName:
        return ItemName(
            jan_code=item.jan_code, name=item.name, updated_at=item.updated_at
        )

    @classmethod
    def toItemCategory(cls, item: Item) -> ItemCategory:
        return ItemCategory(
            jan_code=item.jan_code, category=item.category, updated_at=item.updated_at
        )

    @classmethod
    def toItemMemo(cls, item: Item) -> ItemMemo:
        return ItemMemo(id=item.id, text=item.text, updated_at=item.updated_at)

    @classmethod
    def toItemManufacturer(cls, item: Item) -> ItemManufacturer:
        return ItemManufacturer(
            jan_code=item.jan_code,
            manufacturer=item.manufacturer,
            updated_at=item.updated_at,
        )


class JanCodeInfoToDBObject:
    @classmethod
    def toItemName(cls, jancodeinfo: JanCodeInfo) -> ItemName:
        return ItemName(
            jan_code=jancodeinfo.jan_code,
            name=jancodeinfo.name,
            updated_at=jancodeinfo.updated_at,
        )

    @classmethod
    def toItemCategory(cls, jancodeinfo: JanCodeInfo) -> ItemCategory:
        return ItemCategory(
            jan_code=jancodeinfo.jan_code,
            category=jancodeinfo.category,
            updated_at=jancodeinfo.updated_at,
        )

    @classmethod
    def toItemManufacturer(cls, jancodeinfo: JanCodeInfo) -> ItemManufacturer:
        return ItemManufacturer(
            jan_code=jancodeinfo.jan_code,
            manufacturer=jancodeinfo.manufacturer,
            updated_at=jancodeinfo.updated_at,
        )


class DBToItem:
    factory: IItemFactory

    def __init__(self, factory: IItemFactory):
        self.factory = factory

    def toItem(
        self,
        item_inventory: ItemInventory,
        item_name: ItemName,
        item_category: ItemCategory,
        item_memo: ItemMemo,
        item_manufacturer: ItemManufacturer,
    ) -> Item:
        return self.factory.create(
            id=item_inventory.id,
            name=item_name.name,
            jan_code=item_inventory.jan_code,
            inventory=item_inventory.inventory,
            place=item_inventory.place,
            category=item_category.category,
            manufacturer=item_manufacturer.manufacturer,
            text=item_memo.text,
            expiry_date=item_inventory.expiry_date,
            created_at=item_inventory.created_at,
            updated_at=item_inventory.updated_at,
        )


class DBToJanCodeInfo:
    jancodeinfofactory: IJanCodeInfoFactory

    def __init__(self, factory: IJanCodeInfoFactory):
        self.jancodeinfofactory = factory

    def toJanCodeInfo(
        self,
        item_name: ItemName,
        item_category: ItemCategory,
        item_manufacturer: ItemManufacturer,
    ) -> JanCodeInfo:
        updl: list = []
        if item_name.updated_at:
            updl.append(item_name.updated_at)
        if item_category.updated_at:
            updl.append(item_category.updated_at)
        if item_manufacturer.updated_at:
            updl.append(item_manufacturer.updated_at)
        return self.jancodeinfofactory.create(
            jan_code=item_name.jan_code,
            name=item_name.name,
            category=item_category.category,
            manufacturer=item_manufacturer.manufacturer,
            updated_at=max(updl),
        )
