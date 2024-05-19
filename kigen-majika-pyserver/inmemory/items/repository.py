from domain.models import (
    Item,
    JanCode,
    JanCodeInfo,
    IItemRepository,
    IJanCodeInfoRepository,
)


class ItemDictRepository(IItemRepository):
    database: dict[int, Item]

    def __init__(self, data: dict[int, Item]):
        self.database = data

    async def save(self, item: Item):
        self.database[item.id] = item

    async def find_by_jan_code(self, jan_code: JanCode) -> list[Item]:
        results: list[Item] = []
        for v in self.database.values():
            if v.jan_code == jan_code:
                results.append(v)
        return results

    async def find_by_id(self, id: int) -> Item | None:
        return self.database.get(id, None)

    async def find_all(self) -> list[Item]:
        return list(self.database.values())

    async def delete_by_id(self, id: int) -> None:
        if id not in self.database:
            return None
        item = self.database.pop(id)
        return


class JanCodeInfoDictRepository(IJanCodeInfoRepository):
    database: dict[str, JanCodeInfo]

    def __init__(self, data: dict[str, JanCodeInfo]):
        self.database = data

    async def save(self, jancodeinfo: JanCodeInfo):
        self.database[jancodeinfo.jan_code.value] = jancodeinfo

    async def find_by_jan_code(self, jan_code: JanCode) -> JanCodeInfo | None:
        return self.database.get(jan_code.value, None)
