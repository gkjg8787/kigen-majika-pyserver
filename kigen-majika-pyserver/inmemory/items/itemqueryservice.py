from domain.models import Item, ItemSort, ItemStockFilter
from domain.service import ItemSortService, ItemStockFilterService


from application.items import IItemQueryService, ItemQueryCommand, ItemQueryResult


class ItemQueryDictService(IItemQueryService):
    database: dict[int, Item]

    def __init__(self, data: dict):
        self.database = data

    async def find_all(self, itemquerycommand: ItemQueryCommand) -> ItemQueryResult:
        results: list[Item] = []
        for k, v in self.database.items():
            if itemquerycommand.stock:
                if not await self.is_stock(itemquerycommand=itemquerycommand, item=v):
                    continue
            results.append(v)
        if itemquerycommand.isort:
            results = await self.sort_items(
                itemquerycommand=itemquerycommand, items=results
            )
        return ItemQueryResult(items=results)

    async def is_stock(self, itemquerycommand: ItemQueryCommand, item: Item):
        stockfilter_type: ItemStockFilter = await ItemStockFilterService().get(
            stock_id=itemquerycommand.stock
        )
        if not stockfilter_type:
            return True
        match stockfilter_type:
            case ItemStockFilter.ALL:
                return True
            case ItemStockFilter.IN_STOCK:
                return item.inventory > 0
            case ItemStockFilter.NO_STOCK:
                return item.inventory == 0
        return True

    async def sort_items(
        self, itemquerycommand: ItemQueryCommand, items: list[Item]
    ) -> list[Item]:
        def get_default_order_by(items: list[Item]):
            return sorted(items, key=lambda i: i.expiry_date)

        isort_type: ItemSort = await ItemSortService().get(
            sort_id=itemquerycommand.isort
        )
        if not isort_type:
            return get_default_order_by(items)
        match isort_type:
            case ItemSort.NEAR_EXPIRY:
                return get_default_order_by(items)
            case ItemSort.FAR_EXPIRY:
                return sorted(items, key=lambda i: i.expiry_date, reverse=True)
            case ItemSort.OLD_REGIST:
                return sorted(items, key=lambda i: i.created_at)
            case ItemSort.NEW_REGIST:
                return sorted(items, key=lambda i: i.created_at, reverse=True)
            case ItemSort.ITEMNAME_ASC:
                return sorted(items, key=lambda i: i.name)
            case ItemSort.ITEMNAME_DESC:
                return sorted(items, key=lambda i: i.name, reverse=True)
        return get_default_order_by(items)
