import os
from datetime import datetime, timezone
import pytest

from model.service.jancode_item import JanSyohinKensakuResult, JanCodeInfoData
from model.service import OnlineJanCodeInfoCreator
from model.domain import JanCodeInfo, JanCodeInfoFactory


def assert_comparing_jancodeinfo(one: JanCodeInfo, two: JanCodeInfo):
    assert one.jan_code == two.jan_code
    assert one.name == two.name
    assert one.category == two.category
    assert one.manufacturer == two.manufacturer


class TestJanSyohinKensakuResult:
    BASE = os.path.dirname(__file__)
    test_filename = BASE + "/jansyohinkensaku.html"
    test_filename_no_jancode = BASE + "/jansyohinkensaku_no_jan.html"

    def test_toJanCodeInfo_data_exist(self):
        html = ""
        with open(self.test_filename) as f:
            html = f.read()
        assert html != ""
        jan_code = "4902121033850"
        parse_jancodeinfo = JanSyohinKensakuResult(html).toJanCodeInfo(
            jancodeinfodata=JanCodeInfoData(
                jancodeinfofactory=JanCodeInfoFactory(), jan_code=jan_code
            )
        )
        compjci = JanCodeInfo(
            jan_code=jan_code,
            name="TVBP 穀物酢",
            category="加工食品 調味料",
            manufacturer="イオン",
            updated_at=datetime.now(timezone.utc),
        )
        assert_comparing_jancodeinfo(parse_jancodeinfo, compjci)

    def test_toJanCodeInfo_no_data(self):
        html = ""
        with open(self.test_filename_no_jancode) as f:
            html = f.read()
        assert html != ""
        jan_code = "4"
        parse_jancodeinfo = JanSyohinKensakuResult(html).toJanCodeInfo(
            jancodeinfodata=JanCodeInfoData(
                jancodeinfofactory=JanCodeInfoFactory(), jan_code=jan_code
            )
        )
        compjci = JanCodeInfo(
            jan_code=jan_code,
            name="",
            category="",
            manufacturer="",
            updated_at=datetime.now(timezone.utc),
        )
        assert_comparing_jancodeinfo(parse_jancodeinfo, compjci)


class TestOnlineJanCodeInfoCreator:

    @pytest.mark.asyncio
    async def test_create(self, test_db):
        jan_code = "4902121033850"
        get_jancodeinfo = await OnlineJanCodeInfoCreator(
            factory=JanCodeInfoFactory()
        ).create(jan_code)
        compjci = JanCodeInfo(
            jan_code=jan_code,
            name="TVBP 穀物酢",
            category="加工食品 調味料",
            manufacturer="イオン",
            updated_at=datetime.now(timezone.utc),
        )
        assert_comparing_jancodeinfo(get_jancodeinfo, compjci)
