from domain.models import IJanCodeInfoRepository, JanCodeInfo
from application.items import IJanCodeInfoCreator

from pydantic import BaseModel


class JanCodeInfoResult(BaseModel):
    jancodeinfo: JanCodeInfo | None = None
    error_msg: str = ""


class GetJanCodeInfo:
    jancodeinforepository: IJanCodeInfoRepository

    def __init__(self, repository: IJanCodeInfoRepository):
        self.jancodeinforepository = repository

    async def get(self, jan_code: str) -> JanCodeInfoResult:
        if not jan_code:
            return JanCodeInfoResult()
        jancodeinfo = await self.jancodeinforepository.find_by_jan_code(
            jan_code=jan_code
        )
        if jancodeinfo:
            return JanCodeInfoResult(jancodeinfo=jancodeinfo)
        return JanCodeInfoResult()


class GetOnlineJanCodeInfo:
    jancodeinforepository: IJanCodeInfoRepository
    jancodeinfocreator: IJanCodeInfoCreator
    get_info_online: bool

    def __init__(
        self,
        repository: IJanCodeInfoRepository,
        jancodeinfocreator: IJanCodeInfoCreator,
        get_info_online: bool = True,
    ):
        self.jancodeinforepository = repository
        self.jancodeinfocreator = jancodeinfocreator
        self.get_info_online = get_info_online

    async def get_or_create(self, jan_code: str) -> JanCodeInfoResult:
        if not jan_code:
            return JanCodeInfoResult()
        if jan_code.isdigit():
            jan_code = str(int(jan_code)).zfill(len(jan_code))
        jancodeinfo = await self.jancodeinforepository.find_by_jan_code(
            jan_code=jan_code
        )
        if jancodeinfo:
            return JanCodeInfoResult(jancodeinfo=jancodeinfo)
        if not self.get_info_online:
            return JanCodeInfoResult()
        jancodeinfo = await self.jancodeinfocreator.create(jan_code=jan_code)
        if jancodeinfo.name or jancodeinfo.category or jancodeinfo.manufacturer:
            await self.jancodeinforepository.save(jancodeinfo=jancodeinfo)
            return JanCodeInfoResult(jancodeinfo=jancodeinfo)
        return JanCodeInfoResult()
