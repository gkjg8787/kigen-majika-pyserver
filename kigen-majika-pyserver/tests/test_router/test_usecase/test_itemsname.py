from datetime import datetime, timezone
from typing import Any, Coroutine

import pytest

from router.usecase import itemsname
from model.service import ItemNameDictRepository, IJanCodeInfoCreator
from model.service.jancode_item import JanCodeInfo
from model.database import ItemName


class TestItemName:
    @pytest.mark.asyncio
    async def test_get_exist_jan_code_one_data(self, test_db):
        jan_code = "0123456789012"
        name = "名無し"
        data: dict[str, ItemName] = {}
        data[jan_code] = ItemName(jan_code=jan_code, name=name)
        ret = await itemsname.ItemName(
            repository=ItemNameDictRepository(data=data)
        ).get(jan_code=jan_code)
        assert ret.jan_code == jan_code
        assert ret.name == name

    @pytest.mark.asyncio
    async def test_get_exist_jan_code_multi_data(self, test_db):
        target_index = 1
        itemname_list = [
            ItemName(jan_code="0000000000001", name="one"),
            ItemName(jan_code="2222222222222", name="two"),
            ItemName(jan_code="3333333333333", name="3"),
        ]
        data: dict[str, ItemName] = {}
        for i in itemname_list:
            data[i.jan_code] = i
        ret = await itemsname.ItemName(
            repository=ItemNameDictRepository(data=data)
        ).get(jan_code=itemname_list[target_index].jan_code)
        assert ret.jan_code == itemname_list[target_index].jan_code
        assert ret.name == itemname_list[target_index].name

    @pytest.mark.asyncio
    async def test_get_not_exist_jan_code(self, test_db):
        jan_code = "0123456789012"
        data: dict[str, ItemName] = {}
        ret = await itemsname.ItemName(
            repository=ItemNameDictRepository(data=data)
        ).get(jan_code=jan_code)
        assert ret.jan_code == jan_code
        assert ret.name is None


class DummyJanCodeInfoCreator(IJanCodeInfoCreator):
    def __init__(self, jancodeinfo: JanCodeInfo):
        self.jancodeinfo = jancodeinfo

    async def create(self, jan_code: str):
        return self.jancodeinfo


class TestOnlineItemName:
    @pytest.mark.asyncio
    async def test_get_or_create_name_in_database(self):
        itemname = ItemName(jan_code="0123456789012", name="test")
        return_jancodeinfo = JanCodeInfo(jan_code=itemname.jan_code, name="dummy")
        data: dict[str, ItemName] = {}
        data[itemname.jan_code] = itemname
        ret = await itemsname.OnlineItemName(
            repository=ItemNameDictRepository(data),
            jancodeinfocreator=DummyJanCodeInfoCreator(jancodeinfo=return_jancodeinfo),
        ).get_or_create(jan_code=itemname.jan_code)
        assert ret.jan_code == itemname.jan_code
        assert ret.name == itemname.name

    @pytest.mark.asyncio
    async def test_get_or_create_name_not_in_database(self):
        itemname = ItemName(jan_code="0123456789012", name="test")
        return_jancodeinfo = JanCodeInfo(jan_code=itemname.jan_code, name="dummy")
        data: dict[str, ItemName] = {}
        ret = await itemsname.OnlineItemName(
            repository=ItemNameDictRepository(data),
            jancodeinfocreator=DummyJanCodeInfoCreator(jancodeinfo=return_jancodeinfo),
        ).get_or_create(jan_code=itemname.jan_code)
        assert ret.jan_code == return_jancodeinfo.jan_code
        assert ret.name == return_jancodeinfo.name
