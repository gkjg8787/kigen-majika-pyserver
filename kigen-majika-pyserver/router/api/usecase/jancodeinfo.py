from domain.models import IItemRepository, Item

from pydantic import BaseModel


class JanCodeInfoResult(BaseModel):
    jan_code: str
    name: str | None = None
    category: str | None = None
    manufacturer: str | None = None
    error_msg: str = ""


class GetJanCodeInfo:
    itemrepository: IItemRepository

    def __init__(self, itemrepository: IItemRepository):
        self.itemrepository = itemrepository

    async def execute(self, jan_code: str) -> JanCodeInfoResult:
        item: Item = await self.itemrepository.find_by_jan_code(jan_code=jan_code)
        if not item:
            return JanCodeInfoResult(error_msg="Not Found Data", jan_code=jan_code)
        return JanCodeInfoResult(
            jan_code=item.jan_code,
            name=item.name,
            category=item.category,
            manufacturer=item.manufacturer,
        )
