from model.database import (
    ItemInventory,
    ItemName,
    ItemMemo,
    ItemCategory,
    ItemManufacturer,
)


class ItemInventoryDataCompare:
    @classmethod
    def equal(cls, inventory1: ItemInventory, inventory2: ItemInventory) -> bool:
        return (
            inventory1.id == inventory2.id
            and inventory1.jan_code == inventory2.jan_code
            and inventory1.inventory == inventory2.inventory
            and inventory1.place == inventory2.place
            and inventory1.expiry_date == inventory2.expiry_date
        )


class ItemNameDataCompare:
    @classmethod
    def equal(cls, name1: ItemName, name2: ItemName) -> bool:
        return name1.jan_code == name2.jan_code and name1.name == name2.name


class ItemCategoryDataCompare:
    @classmethod
    def equal(cls, category1: ItemCategory, category2: ItemCategory) -> bool:
        return (
            category1.jan_code == category2.jan_code
            and category1.category == category2.category
        )


class ItemMemoDataCompare:
    @classmethod
    def equal(cls, memo1: ItemMemo, memo2: ItemMemo) -> bool:
        return memo1.id == memo2.id and memo1.text == memo2.text


class ItemManufacturerDataCompare:
    @classmethod
    def equal(cls, manu1: ItemManufacturer, manu2: ItemManufacturer) -> bool:
        return (
            manu1.jan_code == manu2.jan_code
            and manu1.manufacturer == manu2.manufacturer
        )
