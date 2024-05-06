from datetime import datetime, timezone
import pytest

from model.service import (
    ItemNameRepository,
    ItemRepository,
    ItemCategoryRepository,
    ItemManufacturerRepository,
)
from model.domain import (
    ItemNameData,
    ItemFactory,
    Item,
    ItemCategoryData,
    ItemManufacturerData,
)
from model.database import (
    ItemName,
    ItemCategory,
    ItemInventory,
    ItemMemo,
    ItemManufacturer,
)


class TestItemNameRepository:
    @pytest.mark.asyncio
    async def test_save(self, test_db):
        name = "test"
        jan_code = "012345678912"
        async for db in test_db:
            repo = ItemNameRepository(db)
            ind = ItemNameData(name=name, jan_code=jan_code)
            await repo.save(ind)
            ret: ItemName = await db.get(ItemName, jan_code)
            assert ret
            compitemname = ItemName(name=name, jan_code=jan_code)
            assert ret.jan_code == compitemname.jan_code
            assert ret.name == compitemname.name

    @pytest.mark.asyncio
    async def test_find_by_jan_code(self, test_db):
        name = "test"
        jan_code = "0123456789012"
        async for db in test_db:
            repo = ItemNameRepository(db)
            itemname = ItemName(jan_code=jan_code, name=name)
            db.add(itemname)
            await db.commit()
            ret = await repo.find_by_jan_code(jan_code=jan_code)
            assert ret
            assert ret.jan_code == itemname.jan_code
            assert ret.name == itemname.name


class TestItemRepository:

    @classmethod
    def get_one_item(
        cls,
        id: int = 1,
        name: str = "test",
        jan_code: str = "0123456789012",
        inventry: int = 1,
        place: str = "closet",
        category: str = "any",
        manufacturer: str = "maker",
        text: str = "memo",
        expiry_date: datetime | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> Item:
        now = datetime.now(timezone.utc)
        if created_at is None:
            created_at = now
        if updated_at is None:
            updated_at = now
        return ItemFactory.create(
            id=id,
            name=name,
            jan_code=jan_code,
            inventory=inventry,
            place=place,
            category=category,
            manufacturer=manufacturer,
            text=text,
            expiry_date=expiry_date,
            created_at=created_at,
            updated_at=updated_at,
        )

    async def assert_comparing_item(self, db, item: Item):
        iname: ItemName = await db.get(ItemName, item.jan_code)
        iinv: ItemInventory = await db.get(ItemInventory, item.id)
        icate: ItemCategory = await db.get(ItemCategory, item.jan_code)
        imanu: ItemManufacturer = await db.get(ItemManufacturer, item.jan_code)
        imemo: ItemMemo = await db.get(ItemMemo, item.id)
        assert iname.jan_code == item.jan_code
        assert iname.name == item.name

        assert iinv.id == item.id
        assert iinv.inventory == item.inventory
        assert iinv.place == item.place
        date_format = "%Y/%m/%d %H:%M:%S.%f"
        if iinv.expiry_date and item.expiry_date:
            assert iinv.expiry_date.strftime(date_format) == item.expiry_date.strftime(
                date_format
            )
        else:
            assert iinv.expiry_date == item.expiry_date

        assert icate.jan_code == item.jan_code
        assert icate.category == item.category

        assert imanu.jan_code == item.jan_code
        assert imanu.manufacturer == item.manufacturer

        assert imemo.id == item.id
        assert imemo.text == item.text

    @pytest.mark.asyncio
    async def test_save(self, test_db):
        async for db in test_db:
            repo = ItemRepository(db)
            item: Item = self.get_one_item()
            await repo.save(item)
            await self.assert_comparing_item(db=db, item=item)

    @pytest.mark.asyncio
    async def test_save_update_name(self, test_db):
        async for db in test_db:
            repo = ItemRepository(db)
            item: Item = self.get_one_item()
            await repo.save(item)
            item.name = "aaa"
            await repo.save(item)
            await self.assert_comparing_item(db=db, item=item)

    @pytest.mark.asyncio
    async def test_save_update_inventory(self, test_db):
        async for db in test_db:
            repo = ItemRepository(db)
            item: Item = self.get_one_item()
            await repo.save(item)
            item.inventory = 99
            item.place = "another"
            item.expiry_date = datetime(2023, 10, 9, 10, 00, 00, tzinfo=timezone.utc)
            await repo.save(item)
            await self.assert_comparing_item(db=db, item=item)

    @pytest.mark.asyncio
    async def test_save_update_category(self, test_db):
        async for db in test_db:
            repo = ItemRepository(db)
            item: Item = self.get_one_item()
            await repo.save(item)
            item.category = "xxx"
            await repo.save(item)
            await self.assert_comparing_item(db=db, item=item)

    @pytest.mark.asyncio
    async def test_save_update_manufacturer(self, test_db):
        async for db in test_db:
            repo = ItemRepository(db)
            item: Item = self.get_one_item()
            await repo.save(item)
            item.manufacturer = "xxx"
            await repo.save(item)
            await self.assert_comparing_item(db=db, item=item)

    @pytest.mark.asyncio
    async def test_save_update_memo(self, test_db):
        async for db in test_db:
            repo = ItemRepository(db)
            item: Item = self.get_one_item()
            await repo.save(item)
            item.text = "kore ha memo desu."
            await repo.save(item)
            await self.assert_comparing_item(db=db, item=item)

    @pytest.mark.asyncio
    async def test_save_update_all(self, test_db):
        async for db in test_db:
            repo = ItemRepository(db)
            item: Item = self.get_one_item()
            await repo.save(item)
            item.name = "おいしい酢"
            item.inventory = 20
            item.place = "倉庫"
            item.category = "酢"
            item.manufacturer = "〇オン"
            item.text = "存在しない"
            item.expiry_date = datetime(2026, 10, 9, 10, 00, 00, tzinfo=timezone.utc)
            await repo.save(item)
            await self.assert_comparing_item(db=db, item=item)

    @classmethod
    def assert_comparing_two_items(cls, one: Item, two: Item):
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

    @pytest.mark.asyncio
    async def test_find_by_jan_code_one_data(self, test_db):
        async for db in test_db:
            repo = ItemRepository(db)
            item: Item = self.get_one_item(
                expiry_date=datetime(2024, 12, 30, 0, 0, 0, tzinfo=timezone.utc)
            )
            await repo.save(item)

            ret = await repo.find_by_jan_code(item.jan_code)
            assert len(ret) == 1
            self.assert_comparing_two_items(ret[0], item)

    @pytest.mark.asyncio
    async def test_find_by_id_one_data(self, test_db):
        async for db in test_db:
            repo = ItemRepository(db)
            item: Item = self.get_one_item()
            await repo.save(item)

            ret = await repo.find_by_id(item.id)
            assert ret
            self.assert_comparing_two_items(ret, item)

    @pytest.mark.asyncio
    async def test_find_all_three_data(self, test_db):
        def create_item(id: int):
            jan_code = str(id).zfill(13)
            return self.get_one_item(
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

            ret = await repo.find_all()
            assert len(ret) == 3
            for r, i in zip(ret, itemlist):
                self.assert_comparing_two_items(r, i)

    @pytest.mark.asyncio
    async def test_delete_by_id(self, test_db):
        def create_item(id: int):
            jan_code = str(id).zfill(13)
            return self.get_one_item(
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
            target_index = 0
            await repo.delete_by_id(itemlist[target_index].id)
            ret = await repo.find_by_id(itemlist[target_index].id)
            assert ret is None

            rets = await repo.find_all()
            assert len(rets) == 2
            for r in rets:
                assert r.id != itemlist[target_index].id
