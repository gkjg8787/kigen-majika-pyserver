from datetime import datetime, timezone

import pytest

from router.usecase import GetJanCodeInfo, GetOnlineJanCodeInfo
from model.service import JanCodeInfoDictRepository, IJanCodeInfoCreator
from model.domain import JanCodeInfo, JanCodeInfoFactory


class TestGetJanCodeInfo:
    @pytest.mark.asyncio
    async def test_get_exist_jancodeinfo_one_data(self, test_db):
        jan_code = "0123456789012"
        name = "名無し"
        category = "no category"
        manufacturer = "maker"
        updated_at = datetime.now(timezone.utc)
        data: dict[str, JanCodeInfo] = {}
        jancodeinfo = JanCodeInfoFactory.create(
            jan_code=jan_code,
            name=name,
            category=category,
            manufacturer=manufacturer,
            updated_at=updated_at,
        )
        data[jan_code] = jancodeinfo
        ret = await GetJanCodeInfo(repository=JanCodeInfoDictRepository(data=data)).get(
            jan_code=jan_code
        )
        assert ret.jancodeinfo == jancodeinfo

    @pytest.mark.asyncio
    async def test_get_exist_jancodeinfo_multi_data(self, test_db):
        target_index = 0
        data_list: list[JanCodeInfo] = [
            JanCodeInfoFactory.create(
                jan_code="1111111111111",
                name="one",
                category="cate1",
                manufacturer="",
                updated_at=datetime.now(timezone.utc),
            ),
            JanCodeInfoFactory.create(
                jan_code="222222222222",
                name="two",
                category="cate2",
                manufacturer="maker2",
                updated_at=datetime.now(timezone.utc),
            ),
            JanCodeInfoFactory.create(
                jan_code="333333333333",
                name="three",
                category="cate3",
                manufacturer="maker3",
                updated_at=datetime.now(timezone.utc),
            ),
        ]
        ret = await GetJanCodeInfo(
            repository=JanCodeInfoDictRepository(
                data={d.jan_code: d for d in data_list}
            )
        ).get(jan_code=data_list[target_index].jan_code)
        assert ret.jancodeinfo == data_list[target_index]


class DummyJanCodeInfoCreator(IJanCodeInfoCreator):
    def __init__(self, jancodeinfo: JanCodeInfo):
        self.jancodeinfo = jancodeinfo

    async def create(self, jan_code: str):
        return self.jancodeinfo


class TestGetOnlineJanCodeInfo:
    @pytest.mark.asyncio
    async def test_get_or_create_jancodeinfo_in_database(self):
        jancodeinfo = JanCodeInfoFactory.create(
            jan_code="1111111111111",
            name="test",
            category="category",
            manufacturer="manufacturer",
            updated_at=datetime.now(timezone.utc),
        )
        online_jancodeinfo = JanCodeInfoFactory.create(
            jan_code="1111111111111",
            name="online name",
            category="online category",
            manufacturer="online manufacturer",
            updated_at=datetime.now(timezone.utc),
        )
        ret = await GetOnlineJanCodeInfo(
            repository=JanCodeInfoDictRepository(
                data={jancodeinfo.jan_code: jancodeinfo}
            ),
            jancodeinfocreator=DummyJanCodeInfoCreator(jancodeinfo=online_jancodeinfo),
            get_info_online=True,
        ).get_or_create(jan_code=jancodeinfo.jan_code)
        assert ret.jancodeinfo == jancodeinfo

    @pytest.mark.asyncio
    async def test_get_or_create_jancodeinfo_not_in_database(self):
        jan_code = "1111111111111"
        online_jancodeinfo = JanCodeInfoFactory.create(
            jan_code="1111111111111",
            name="online name",
            category="online category",
            manufacturer="online manufacturer",
            updated_at=datetime.now(timezone.utc),
        )
        ret = await GetOnlineJanCodeInfo(
            repository=JanCodeInfoDictRepository(data={}),
            jancodeinfocreator=DummyJanCodeInfoCreator(jancodeinfo=online_jancodeinfo),
            get_info_online=True,
        ).get_or_create(jan_code=jan_code)
        assert ret.jancodeinfo == online_jancodeinfo
