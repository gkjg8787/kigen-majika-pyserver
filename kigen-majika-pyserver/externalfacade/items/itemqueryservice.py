from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from domain.models import Item, ItemSort, ItemStockFilter
from domain.service import ItemSortService, ItemStockFilterService
from .items import (
    ItemInventory,
    ItemCategory,
    ItemManufacturer,
    ItemMemo,
    ItemName,
)
from .factory import ItemFactory
from .dbconvert import DBToItem

from application.items import IItemQueryService, ItemQueryCommand, ItemQueryResult


class ItemQueryService(IItemQueryService):
    session: AsyncSession

    def __init__(self, db: AsyncSession):
        self.session = db

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

    async def find_all(self, itemquerycommand: ItemQueryCommand) -> ItemQueryResult:
        db = self.session
        stmt = (
            select(ItemInventory, ItemName, ItemCategory, ItemManufacturer, ItemMemo)
            .select_from(ItemInventory)
            .join(ItemName, ItemInventory.jan_code == ItemName.jan_code)
            .join(ItemCategory, ItemInventory.jan_code == ItemCategory.jan_code)
            .join(ItemManufacturer, ItemInventory.jan_code == ItemManufacturer.jan_code)
            .join(ItemMemo, ItemInventory.id == ItemMemo.id)
        )
        stmt = await self.get_stockfilter_stmt(
            itemquerycommand=itemquerycommand, stmt=stmt
        )
        stmt = await self.get_sort_stmt(itemquerycommand=itemquerycommand, stmt=stmt)
        ret = await db.execute(stmt)
        return ItemQueryResult(items=self._to_items(ret.mappings().all()))

    async def get_stockfilter_stmt(self, itemquerycommand: ItemQueryCommand, stmt):
        def get_default_stockfilter(stmt):
            return stmt

        if not itemquerycommand.stock:
            return get_default_stockfilter(stmt)
        stockfilter_type: ItemStockFilter = await ItemStockFilterService().get(
            stock_id=itemquerycommand.stock
        )
        if not stockfilter_type:
            return get_default_stockfilter(stmt)
        match stockfilter_type:
            case ItemStockFilter.ALL:
                return get_default_stockfilter(stmt)
            case ItemStockFilter.IN_STOCK:
                return stmt.where(ItemInventory.inventory > 0)
            case ItemStockFilter.NO_STOCK:
                return stmt.where(ItemInventory.inventory == 0)
        return get_default_stockfilter(stmt)

    async def get_sort_stmt(self, itemquerycommand: ItemQueryCommand, stmt):
        def get_default_order_by(stmt):
            return stmt.order_by(ItemInventory.expiry_date.asc())

        if not itemquerycommand.isort:
            return get_default_order_by(stmt)
        isort_type: ItemSort = await ItemSortService().get(
            sort_id=itemquerycommand.isort
        )
        if not isort_type:
            return get_default_order_by(stmt)
        match isort_type:
            case ItemSort.NEAR_EXPIRY:
                return get_default_order_by(stmt)
            case ItemSort.FAR_EXPIRY:
                return stmt.order_by(ItemInventory.expiry_date.desc())
            case ItemSort.OLD_REGIST:
                return stmt.order_by(ItemInventory.created_at.asc())
            case ItemSort.NEW_REGIST:
                return stmt.order_by(ItemInventory.created_at.desc())
            case ItemSort.ITEMNAME_ASC:
                return stmt.order_by(ItemName.name.asc())
            case ItemSort.ITEMNAME_DESC:
                return stmt.order_by(ItemName.name.desc())
        return get_default_order_by(stmt)
