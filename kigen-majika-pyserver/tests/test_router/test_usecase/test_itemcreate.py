from datetime import datetime, timezone

import pytest
from pydantic import BaseModel

from router.usecase.api import itemcreate
from model.domain import ItemFactory
from model.service import ItemDictRepository, ItemDictIdentity

from router.param import ItemCreateParam

from .shared import ItemComparingData


class TestItemCreate:
    async def create_item_and_assert(
        self, icp: ItemCreateParam, error_msg: str, correct_item: ItemComparingData
    ):
        database: dict = {}
        ret = await itemcreate.ItemCreate(
            itemrepository=ItemDictRepository(data=database),
            itemfactory=ItemFactory(),
            itemidentity=ItemDictIdentity(data=database),
        ).create(itemcreateparam=icp)

        assert error_msg == ret.error_msg
        assert correct_item == ItemComparingData(**ret.item.model_dump())

    @staticmethod
    def create_ItemComparingData(
        jan_code: str,
        name=None,
        inventory=None,
        place=None,
        category=None,
        manufacturer=None,
        text=None,
        expiry_date=None,
    ) -> ItemComparingData:
        now = datetime.now(timezone.utc)
        item = ItemFactory.create(
            id=1,
            name=name,
            jan_code=jan_code,
            inventory=inventory,
            place=place,
            category=category,
            manufacturer=manufacturer,
            text=text,
            expiry_date=expiry_date,
            created_at=now,
            updated_at=now,
        )
        return ItemComparingData(**item.model_dump())

    @pytest.mark.asyncio
    async def test_create_all_param(self, test_db):
        icp = ItemCreateParam(
            name="test",
            jan_code="0123456789012",
            inventory=1,
            place="other",
            category="None",
            manufacturer="maker",
            text="five",
            expiry_date=datetime(2024, 11, 30, 0, 0, 0),
        )
        await self.create_item_and_assert(
            icp=icp, error_msg="", correct_item=ItemComparingData(**icp.model_dump())
        )

    @pytest.mark.asyncio
    async def test_create_jancode(self, test_db):
        jan_code = "0123456789012"
        icp = ItemCreateParam(
            jan_code=jan_code,
        )
        correct_item = self.create_ItemComparingData(jan_code=jan_code)
        await self.create_item_and_assert(
            icp=icp,
            error_msg="",
            correct_item=correct_item,
        )

    @pytest.mark.asyncio
    async def test_create_name(self, test_db):
        jan_code = "0123456789012"
        name = "海苔"
        icp = ItemCreateParam(jan_code=jan_code, name=name)
        correct_item = self.create_ItemComparingData(jan_code=jan_code, name=name)
        await self.create_item_and_assert(
            icp=icp,
            error_msg="",
            correct_item=correct_item,
        )

    @pytest.mark.asyncio
    async def test_create_inventory(self, test_db):
        jan_code = "0123456789012"
        inventory = 2
        icp = ItemCreateParam(jan_code=jan_code, inventory=inventory)
        correct_item = self.create_ItemComparingData(
            jan_code=jan_code, inventory=inventory
        )
        await self.create_item_and_assert(
            icp=icp,
            error_msg="",
            correct_item=correct_item,
        )

    @pytest.mark.asyncio
    async def test_create_place(self, test_db):
        jan_code = "0123456789012"
        place = "台所"
        icp = ItemCreateParam(jan_code=jan_code, place=place)
        correct_item = self.create_ItemComparingData(jan_code=jan_code, place=place)
        await self.create_item_and_assert(
            icp=icp,
            error_msg="",
            correct_item=correct_item,
        )

    @pytest.mark.asyncio
    async def test_create_category(self, test_db):
        jan_code = "0123456789012"
        category = "調味料"
        icp = ItemCreateParam(jan_code=jan_code, category=category)
        correct_item = self.create_ItemComparingData(
            jan_code=jan_code, category=category
        )
        await self.create_item_and_assert(
            icp=icp,
            error_msg="",
            correct_item=correct_item,
        )

    @pytest.mark.asyncio
    async def test_create_manufacturer(self, test_db):
        jan_code = "0123456789012"
        manufacturer = "〇オン"
        icp = ItemCreateParam(jan_code=jan_code, manufacturer=manufacturer)
        correct_item = self.create_ItemComparingData(
            jan_code=jan_code, manufacturer=manufacturer
        )
        await self.create_item_and_assert(
            icp=icp,
            error_msg="",
            correct_item=correct_item,
        )

    @pytest.mark.asyncio
    async def test_create_text(self, test_db):
        jan_code = "0123456789012"
        text = "備考欄"
        icp = ItemCreateParam(jan_code=jan_code, text=text)
        correct_item = self.create_ItemComparingData(jan_code=jan_code, text=text)
        await self.create_item_and_assert(
            icp=icp,
            error_msg="",
            correct_item=correct_item,
        )

    @pytest.mark.asyncio
    async def test_create_expiry_date(self, test_db):
        jan_code = "0123456789012"
        expiry_date = datetime(2024, 9, 12, 0, 12, 30, tzinfo=timezone.utc)
        icp = ItemCreateParam(jan_code=jan_code, expiry_date=expiry_date)
        correct_item = self.create_ItemComparingData(
            jan_code=jan_code, expiry_date=expiry_date
        )
        await self.create_item_and_assert(
            icp=icp,
            error_msg="",
            correct_item=correct_item,
        )
