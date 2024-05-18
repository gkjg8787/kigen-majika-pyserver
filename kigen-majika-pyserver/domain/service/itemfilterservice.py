from domain.models import ItemStockFilter, ItemSort, ItemSearchType


class ItemStockFilterService:
    async def get(self, stock_id: int) -> ItemStockFilter | None:
        for isf in ItemStockFilter:
            if isf.id == stock_id:
                return isf
        return None


class ItemSortService:
    async def get(self, sort_id: int) -> ItemSort | None:
        for isort in ItemSort:
            if isort.id == sort_id:
                return isort
        return None


class ItemSearchTypeService:
    async def get(self, search_type: int) -> ItemSearchType | None:
        for stype in ItemSearchType:
            if stype.id == search_type:
                return stype
        return None
