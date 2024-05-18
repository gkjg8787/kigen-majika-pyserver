from datetime import datetime, timezone

import pytest

from externalfacade.items import ItemQueryService, ItemRepository
from application.items import ItemQueryCommand
from domain.models import Item, ItemSort, ItemStockFilter, ItemSearchType

from . import shared


class TestItemQuerySerice:

    @classmethod
    async def assert_comparing_two_items(cls, one: Item, two: Item):
        assert one.id == two.id
        assert one.name == two.name
        assert one.jan_code == two.jan_code
        assert one.inventory == two.inventory
        assert one.place == two.place
        assert one.category == two.category
        assert one.manufacturer == two.manufacturer
        assert one.text == two.text
        date_format = "%Y/%m/%d %H:%M:%S.%f"
        if one.expiry_date and two.expiry_date:
            assert one.expiry_date.strftime(date_format) == two.expiry_date.strftime(
                date_format
            )
        else:
            assert one.expiry_date == two.expiry_date
        assert one.created_at.strftime(date_format) == two.created_at.strftime(
            date_format
        )
        assert one.updated_at.strftime(date_format) == two.updated_at.strftime(
            date_format
        )

    def create_itemquerycommand(
        self, isort: int = 0, stock: int = 0, stype: int = 0, word=""
    ) -> ItemQueryCommand:
        return ItemQueryCommand(isort=isort, stock=stock, stype=stype, word=word)

    @pytest.mark.asyncio
    async def test_find_all_three_data(self, test_db):
        def create_item(id: int):
            jan_code = str(id).zfill(13)
            return shared.get_item(
                id=id,
                name=str(id),
                jan_code=jan_code,
                expiry_date=datetime(2024, id % 12, 1, tzinfo=timezone.utc),
            )

        async for db in test_db:
            repo = ItemRepository(db)
            itemlist: list[Item] = [create_item(i) for i in range(1, 4)]
            for a in itemlist:
                await repo.save(a)

            iqs = ItemQueryService(db)
            command = self.create_itemquerycommand()
            ret = await iqs.find_all(command)
            ret = ret.items
            assert len(ret) == 3
            for r, i in zip(ret, itemlist):
                await self.assert_comparing_two_items(r, i)

    @classmethod
    def get_items_for_sort(cls):
        items_base = [
            {
                "id": 1,
                "jan_code": str(1).zfill(13),
                "name": "aaa",
                "inventory": 1,
                "expiry_date": None,
                "created_at": datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
            },
            {
                "id": 2,
                "jan_code": str(2).zfill(13),
                "name": "ccc",
                "inventory": 0,
                "expiry_date": datetime(2024, 12, 1, 0, 0, 0, tzinfo=timezone.utc),
                "created_at": datetime(2023, 12, 1, 0, 0, 0, tzinfo=timezone.utc),
            },
            {
                "id": 3,
                "jan_code": str(3).zfill(13),
                "name": "bbb",
                "inventory": 2,
                "expiry_date": datetime(2025, 2, 1, 0, 0, 0, tzinfo=timezone.utc),
                "created_at": datetime(2024, 2, 1, 0, 0, 0, tzinfo=timezone.utc),
            },
            {
                "id": 4,
                "jan_code": str(4).zfill(13),
                "name": "ddd",
                "inventory": 0,
                "expiry_date": datetime(2024, 12, 1, 10, 0, 0, tzinfo=timezone.utc),
                "created_at": datetime(2024, 3, 1, 0, 0, 0, tzinfo=timezone.utc),
            },
            {
                "id": 5,
                "jan_code": str(5).zfill(13),
                "name": "dda",
                "inventory": 50,
                "expiry_date": datetime(2024, 12, 28, 0, 0, 0, tzinfo=timezone.utc),
                "created_at": datetime(2024, 2, 1, 0, 40, 0, tzinfo=timezone.utc),
            },
        ]
        results: list[Item] = []
        for i in items_base:
            results.append(shared.get_item(**i))
        return results

    @pytest.mark.asyncio
    async def test_find_all_sort_near_expiry_date_default(self, test_db):
        itemlist: list[Item] = self.get_items_for_sort()
        async for db in test_db:
            repo = ItemRepository(db)
            for a in itemlist:
                await repo.save(a)

            iqs = ItemQueryService(db)
            command = self.create_itemquerycommand()
            ret = await iqs.find_all(command)
            ret = ret.items
            assert len(ret) == len(itemlist)
            for r, i in zip(ret, sorted(itemlist, key=lambda i: i.expiry_date)):
                await self.assert_comparing_two_items(r, i)

    @pytest.mark.asyncio
    async def test_find_all_sort_near_expiry_date_set(self, test_db):
        itemlist: list[Item] = self.get_items_for_sort()
        async for db in test_db:
            repo = ItemRepository(db)
            for a in itemlist:
                await repo.save(a)

            iqs = ItemQueryService(db)
            command = self.create_itemquerycommand(
                isort=ItemSort.NEAR_EXPIRY.id, stock=0
            )
            ret = await iqs.find_all(command)
            ret = ret.items
            assert len(ret) == len(itemlist)
            for r, i in zip(ret, sorted(itemlist, key=lambda i: i.expiry_date)):
                await self.assert_comparing_two_items(r, i)

    @pytest.mark.asyncio
    async def test_find_all_sort_far_expiry_date(self, test_db):
        itemlist: list[Item] = self.get_items_for_sort()
        async for db in test_db:
            repo = ItemRepository(db)
            for a in itemlist:
                await repo.save(a)

            iqs = ItemQueryService(db)
            command = self.create_itemquerycommand(
                isort=ItemSort.FAR_EXPIRY.id, stock=0
            )
            ret = await iqs.find_all(command)
            ret = ret.items
            assert len(ret) == len(itemlist)
            for r, i in zip(
                ret, sorted(itemlist, key=lambda i: i.expiry_date, reverse=True)
            ):
                await self.assert_comparing_two_items(r, i)

    @pytest.mark.asyncio
    async def test_find_all_sort_old_regist(self, test_db):
        itemlist: list[Item] = self.get_items_for_sort()
        async for db in test_db:
            repo = ItemRepository(db)
            for a in itemlist:
                await repo.save(a)

            iqs = ItemQueryService(db)
            command = self.create_itemquerycommand(
                isort=ItemSort.OLD_REGIST.id, stock=0
            )
            ret = await iqs.find_all(command)
            ret = ret.items
            assert len(ret) == len(itemlist)
            for r, i in zip(ret, sorted(itemlist, key=lambda i: i.created_at)):
                await self.assert_comparing_two_items(r, i)

    @pytest.mark.asyncio
    async def test_find_all_sort_new_regist(self, test_db):
        itemlist: list[Item] = self.get_items_for_sort()
        async for db in test_db:
            repo = ItemRepository(db)
            for a in itemlist:
                await repo.save(a)

            iqs = ItemQueryService(db)
            command = self.create_itemquerycommand(
                isort=ItemSort.NEW_REGIST.id, stock=0
            )
            ret = await iqs.find_all(command)
            ret = ret.items
            assert len(ret) == len(itemlist)
            for r, i in zip(
                ret, sorted(itemlist, key=lambda i: i.created_at, reverse=True)
            ):
                await self.assert_comparing_two_items(r, i)

    @pytest.mark.asyncio
    async def test_find_all_sort_itemname_asc(self, test_db):
        itemlist: list[Item] = self.get_items_for_sort()
        async for db in test_db:
            repo = ItemRepository(db)
            for a in itemlist:
                await repo.save(a)

            iqs = ItemQueryService(db)
            command = self.create_itemquerycommand(
                isort=ItemSort.ITEMNAME_ASC.id, stock=0
            )
            ret = await iqs.find_all(command)
            ret = ret.items
            assert len(ret) == len(itemlist)
            for r, i in zip(ret, sorted(itemlist, key=lambda i: i.name)):
                await self.assert_comparing_two_items(r, i)

    @pytest.mark.asyncio
    async def test_find_all_sort_itemname_desc(self, test_db):
        itemlist: list[Item] = self.get_items_for_sort()
        async for db in test_db:
            repo = ItemRepository(db)
            for a in itemlist:
                await repo.save(a)

            iqs = ItemQueryService(db)
            command = self.create_itemquerycommand(
                isort=ItemSort.ITEMNAME_DESC.id, stock=0
            )
            ret = await iqs.find_all(command)
            ret = ret.items
            assert len(ret) == len(itemlist)
            for r, i in zip(ret, sorted(itemlist, key=lambda i: i.name, reverse=True)):
                await self.assert_comparing_two_items(r, i)

    @pytest.mark.asyncio
    async def test_find_all_stock_in_stock(self, test_db):
        def get_stock_items(items: list[Item]):
            return [i for i in items if i.inventory > 0]

        itemlist: list[Item] = self.get_items_for_sort()
        async for db in test_db:
            repo = ItemRepository(db)
            for a in itemlist:
                await repo.save(a)

            iqs = ItemQueryService(db)
            command = self.create_itemquerycommand(
                stock=ItemStockFilter.IN_STOCK.id, isort=0
            )
            ret = await iqs.find_all(command)
            ret = ret.items
            comparing_list = get_stock_items(itemlist)
            assert len(ret) == len(comparing_list)
            for r, i in zip(ret, sorted(comparing_list, key=lambda i: i.expiry_date)):
                await self.assert_comparing_two_items(r, i)

    @pytest.mark.asyncio
    async def test_find_all_stock_no_stock(self, test_db):
        def get_no_stock_items(items: list[Item]):
            return [i for i in items if i.inventory == 0]

        itemlist: list[Item] = self.get_items_for_sort()
        async for db in test_db:
            repo = ItemRepository(db)
            for a in itemlist:
                await repo.save(a)

            iqs = self.create_itemquerycommand(db)
            command = ItemQueryCommand(stock=ItemStockFilter.NO_STOCK.id, isort=0)
            ret = await iqs.find_all(command)
            ret = ret.items
            comparing_list = get_no_stock_items(itemlist)
            assert len(ret) == len(comparing_list)
            for r, i in zip(ret, sorted(comparing_list, key=lambda i: i.expiry_date)):
                await self.assert_comparing_two_items(r, i)

    @classmethod
    def get_items_for_keyword_search(cls) -> list[Item]:
        items_base = [
            {
                "id": 1,
                "jan_code": str(1).zfill(13),
                "name": "aaa",
                "place": "a_place",
                "category": "a_cate",
                "manufacturer": "a_maker",
                "text": "a_text",
            },
            {
                "id": 2,
                "jan_code": str(2).zfill(13),
                "name": "bbb",
                "place": "b_place",
                "category": "b_cate",
                "manufacturer": "b_maker",
                "text": "b_text",
            },
            {
                "id": 3,
                "jan_code": str(1).zfill(13),
                "name": "aaa",
                "place": "b_place",
                "category": "a_cate",
                "manufacturer": "a_maker",
                "text": "c_text",
            },
            {
                "id": 4,
                "jan_code": str(4).zfill(13),
                "name": "ccc",
                "place": "c_place",
                "category": "c_cate",
                "manufacturer": "c_maker",
                "text": "c_text",
            },
        ]
        results: list[Item] = []
        for i in items_base:
            results.append(shared.get_item(**i))
        return results

    @pytest.mark.asyncio
    async def test_find_all_keyword_search_name(self, test_db):
        def get_comparing_items(items: list[Item]):
            return [i for i in items if "aaa" in i.name]

        itemlist: list[Item] = self.get_items_for_keyword_search()
        async for db in test_db:
            repo = ItemRepository(db)
            for a in itemlist:
                await repo.save(a)

            iqs = ItemQueryService(db)
            command = self.create_itemquerycommand(
                stype=ItemSearchType.NAME.id, word="aaa"
            )
            ret = await iqs.find_all(command)
            ret = ret.items
            comparing_list = get_comparing_items(itemlist)
            assert len(ret) == len(comparing_list)
            for r, i in zip(ret, comparing_list):
                await self.assert_comparing_two_items(r, i)

    @pytest.mark.asyncio
    async def test_find_all_keyword_search_jancode(self, test_db):
        def get_comparing_items(items: list[Item]):
            return [i for i in items if str(2).zfill(13) in i.jan_code]

        itemlist: list[Item] = self.get_items_for_keyword_search()
        async for db in test_db:
            repo = ItemRepository(db)
            for a in itemlist:
                await repo.save(a)

            iqs = ItemQueryService(db)
            command = self.create_itemquerycommand(
                stype=ItemSearchType.JANCODE.id, word=str(2).zfill(13)
            )
            ret = await iqs.find_all(command)
            ret = ret.items
            comparing_list = get_comparing_items(itemlist)
            assert len(ret) == len(comparing_list)
            for r, i in zip(ret, comparing_list):
                await self.assert_comparing_two_items(r, i)

    @pytest.mark.asyncio
    async def test_find_all_keyword_search_category(self, test_db):
        def get_comparing_items(items: list[Item]):
            return [i for i in items if "c_cate" in i.category]

        itemlist: list[Item] = self.get_items_for_keyword_search()
        async for db in test_db:
            repo = ItemRepository(db)
            for a in itemlist:
                await repo.save(a)

            iqs = ItemQueryService(db)
            command = self.create_itemquerycommand(
                stype=ItemSearchType.CATEGORY.id, word="c_cate"
            )
            ret = await iqs.find_all(command)
            ret = ret.items
            comparing_list = get_comparing_items(itemlist)
            assert len(ret) == len(comparing_list)
            for r, i in zip(ret, comparing_list):
                await self.assert_comparing_two_items(r, i)

    @pytest.mark.asyncio
    async def test_find_all_keyword_search_manufacturer(self, test_db):
        def get_comparing_items(items: list[Item]):
            return [i for i in items if "b_maker" in i.category]

        itemlist: list[Item] = self.get_items_for_keyword_search()
        async for db in test_db:
            repo = ItemRepository(db)
            for a in itemlist:
                await repo.save(a)

            iqs = ItemQueryService(db)
            command = self.create_itemquerycommand(
                stype=ItemSearchType.MANUFACTURER.id, word="b_maker"
            )
            ret = await iqs.find_all(command)
            ret = ret.items
            comparing_list = get_comparing_items(itemlist)
            assert len(ret) == len(comparing_list)
            for r, i in zip(ret, comparing_list):
                await self.assert_comparing_two_items(r, i)

    @pytest.mark.asyncio
    async def test_find_all_keyword_search_place(self, test_db):
        def get_comparing_items(items: list[Item]):
            return [i for i in items if "a_place" in i.category]

        itemlist: list[Item] = self.get_items_for_keyword_search()
        async for db in test_db:
            repo = ItemRepository(db)
            for a in itemlist:
                await repo.save(a)

            iqs = ItemQueryService(db)
            command = self.create_itemquerycommand(
                stype=ItemSearchType.PLACE.id, word="a_place"
            )
            ret = await iqs.find_all(command)
            ret = ret.items
            comparing_list = get_comparing_items(itemlist)
            assert len(ret) == len(comparing_list)
            for r, i in zip(ret, comparing_list):
                await self.assert_comparing_two_items(r, i)

    @pytest.mark.asyncio
    async def test_find_all_keyword_search_memo(self, test_db):
        def get_comparing_items(items: list[Item]):
            return [i for i in items if "c_text" in i.category]

        itemlist: list[Item] = self.get_items_for_keyword_search()
        async for db in test_db:
            repo = ItemRepository(db)
            for a in itemlist:
                await repo.save(a)

            iqs = ItemQueryService(db)
            command = self.create_itemquerycommand(
                stype=ItemSearchType.MEMO.id, word="c_text"
            )
            ret = await iqs.find_all(command)
            ret = ret.items
            comparing_list = get_comparing_items(itemlist)
            assert len(ret) == len(comparing_list)
            for r, i in zip(ret, comparing_list):
                await self.assert_comparing_two_items(r, i)
