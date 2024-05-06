from abc import ABCMeta, abstractmethod
import re

from pydantic import BaseModel
from bs4 import BeautifulSoup

from .download import async_download_text, DownloadCommand, DownloadType


class JanCodeInfo(BaseModel):
    jan_code: str
    name: str = ""
    category: str = ""
    manufacturer: str = ""


class JanSyohinKensakuResult:
    soup: BeautifulSoup

    def __init__(self, htmltext: str):
        self.soup = BeautifulSoup(htmltext, "html.parser")

    def _trim_str(self, text: str):
        table = str.maketrans({"\u3000": " ", "\r": "", "\n": "", "\t": " "})
        return text.translate(table).strip()

    def toJanCodeInfo(self, jan_code: str) -> JanCodeInfo:
        result = JanCodeInfo(jan_code=jan_code)
        tr_list = self.soup.select("table.goods tr")
        if not tr_list:
            return result
        for tr in tr_list:
            key = tr.select_one("td.goodskey").text
            value = tr.select_one("td.goodsval").text
            match key:
                case "商品名":
                    result.name = self._trim_str(value)
                    continue
                case "メーカ":
                    result.manufacturer = self._trim_str(value)
                    continue
                case "分類":
                    result.category = self._trim_str(value)
                    continue
        return result


class IJanCodeInfoCreator(metaclass=ABCMeta):

    @abstractmethod
    async def create(self, jan_code: str) -> JanCodeInfo:
        pass


class OnlineJanCodeInfoCreator(IJanCodeInfoCreator):
    url = "https://www.janken.jp/gadgets/jan/JanSyohinKensaku.php"

    async def create(self, jan_code: str) -> JanCodeInfo:
        if not jan_code or not jan_code.isdigit():
            return JanCodeInfo(jan_code=jan_code)
        ret = await async_download_text(
            DownloadCommand(
                url=self.url,
                downloadtype=DownloadType.POST,
                params={"dummy": "", "jan": jan_code},
            )
        )
        if not ret:
            return JanCodeInfo(jan_code=jan_code)
        return JanSyohinKensakuResult(ret).toJanCodeInfo(jan_code=jan_code)
