from model.service import IItemNameRepository
from model.service import IJanCodeInfoCreator
from model.domain import ItemNameData

from pydantic import BaseModel


class ItemNameResult(BaseModel):
    jan_code: str
    name: str | None = None
    error_msg: str = ""


class ItemName:
    itemnamerepository: IItemNameRepository

    def __init__(self, repository: IItemNameRepository):
        self.itemnamerepository = repository

    async def get(self, jan_code: str) -> ItemNameResult:
        ret = ItemNameResult(jan_code=jan_code)
        itemname = await self.itemnamerepository.find_by_jan_code(jan_code=jan_code)
        if itemname:
            ret.name = itemname.name
            return ret
        return ret


class OnlineItemName:
    itemnamerepository: IItemNameRepository
    jancodeinfocreator: IJanCodeInfoCreator

    def __init__(
        self, repository: IItemNameRepository, jancodeinfocreator: IJanCodeInfoCreator
    ):
        self.itemnamerepository = repository
        self.jancodeinfocreator = jancodeinfocreator

    async def get_or_create(self, jan_code: str) -> ItemNameResult:
        ret = ItemNameResult(jan_code=jan_code)
        itemname = await self.itemnamerepository.find_by_jan_code(jan_code=jan_code)
        if itemname:
            ret.name = itemname.name
            return ret
        jancodeinfo = await self.jancodeinfocreator.create(jan_code=jan_code)
        if jancodeinfo.name:
            await self.itemnamerepository.save(
                itemnamedata=ItemNameData(jan_code=jan_code, name=jancodeinfo.name)
            )
            ret.name = jancodeinfo.name
            return ret
        return ret
