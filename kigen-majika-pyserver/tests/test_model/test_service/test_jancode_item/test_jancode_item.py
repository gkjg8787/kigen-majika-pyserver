import os

import pytest

from model.service.jancode_item import JanSyohinKensakuResult, JanCodeInfo
from model.service import OnlineJanCodeInfoCreator


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
        parse_jancodeinfo = JanSyohinKensakuResult(html).toJanCodeInfo(jan_code)
        compjci = JanCodeInfo(
            jan_code=jan_code,
            name="TVBP 穀物酢",
            category="加工食品 調味料",
            manufacturer="イオン",
        )
        assert parse_jancodeinfo == compjci

    def test_toJanCodeInfo_no_data(self):
        html = ""
        with open(self.test_filename_no_jancode) as f:
            html = f.read()
        assert html != ""
        jan_code = "4"
        parse_jancodeinfo = JanSyohinKensakuResult(html).toJanCodeInfo(jan_code)
        compjci = JanCodeInfo(
            jan_code=jan_code,
            name="",
            category="",
            manufacturer="",
        )
        assert parse_jancodeinfo == compjci


class TestOnlineJanCodeInfoCreator:

    @pytest.mark.asyncio
    async def test_create(self, test_db):
        jan_code = "4902121033850"
        get_jancodeinfo = await OnlineJanCodeInfoCreator().create(jan_code)
        compjci = JanCodeInfo(
            jan_code=jan_code,
            name="TVBP 穀物酢",
            category="加工食品 調味料",
            manufacturer="イオン",
        )
        assert get_jancodeinfo == compjci
