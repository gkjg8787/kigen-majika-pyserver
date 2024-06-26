from abc import ABCMeta, abstractmethod
from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict
from bs4 import BeautifulSoup

from application.download import async_download_text, DownloadCommand, DownloadType
from domain.models import JanCodeInfo, IJanCodeInfoFactory, JanCode, IJanCodeFactory


class JanCodeInfoData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    jancodeinfofactory: IJanCodeInfoFactory
    jan_code: JanCode
    name: str = ""
    category: str = ""
    manufacturer: str = ""
    updated_at: datetime | None = None

    def toJanCodeInfo(self) -> JanCodeInfo:
        if not self.updated_at:
            self.updated_at = datetime.now(timezone.utc)
        return self.jancodeinfofactory.create(
            jan_code=self.jan_code,
            name=self.name,
            category=self.category,
            manufacturer=self.manufacturer,
            updated_at=self.updated_at,
        )


class JanSyohinKensakuResult:
    soup: BeautifulSoup

    def __init__(self, htmltext: str):
        self.soup = BeautifulSoup(htmltext, "html.parser")

    def _trim_str(self, text: str):
        table = str.maketrans({"\u3000": " ", "\r": "", "\n": "", "\t": " "})
        return text.translate(table).strip()

    def toJanCodeInfo(self, jancodeinfodata: JanCodeInfoData) -> JanCodeInfo:
        tr_list = self.soup.select("table.goods tr")
        if not tr_list:
            return jancodeinfodata.toJanCodeInfo()
        for tr in tr_list:
            key = tr.select_one("td.goodskey").text
            value = tr.select_one("td.goodsval").text
            match key:
                case "商品名":
                    jancodeinfodata.name = self._trim_str(value)
                    continue
                case "メーカ":
                    jancodeinfodata.manufacturer = self._trim_str(value)
                    continue
                case "分類":
                    jancodeinfodata.category = self._trim_str(value)
                    continue
        return jancodeinfodata.toJanCodeInfo()


class IJanCodeInfoCreator(metaclass=ABCMeta):

    @abstractmethod
    async def create(self, jan_code: JanCode) -> JanCodeInfo:
        pass


class OnlineJanCodeInfoCreator(IJanCodeInfoCreator):
    url = "https://www.janken.jp/gadgets/jan/JanSyohinKensaku.php"
    jancodeinfofactory: IJanCodeInfoFactory

    def __init__(self, factory: IJanCodeInfoFactory):
        self.jancodeinfofactory = factory

    async def create(self, jan_code: JanCode) -> JanCodeInfo:
        if not jan_code:
            return JanCodeInfoData(
                jancodeinfofactory=self.jancodeinfofactory, jan_code=jan_code
            ).toJanCodeInfo()
        ret = await async_download_text(
            DownloadCommand(
                url=self.url,
                downloadtype=DownloadType.POST,
                params={"dummy": "", "jan": jan_code.value},
            )
        )
        if not ret:
            return JanCodeInfoData(
                jancodeinfofactory=self.jancodeinfofactory, jan_code=jan_code
            ).toJanCodeInfo()
        return JanSyohinKensakuResult(htmltext=ret).toJanCodeInfo(
            jancodeinfodata=JanCodeInfoData(
                jancodeinfofactory=self.jancodeinfofactory, jan_code=jan_code
            )
        )
