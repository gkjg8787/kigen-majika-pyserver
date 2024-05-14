from abc import ABCMeta, abstractmethod

from .items import Item, JanCodeInfo


class IItemRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, item: Item):
        pass

    @abstractmethod
    async def find_by_jan_code(self, jan_code: str) -> list[Item]:
        pass

    @abstractmethod
    async def find_by_id(self, id: int) -> Item | None:
        pass

    @abstractmethod
    async def find_all(self) -> list[Item]:
        pass

    @abstractmethod
    async def delete_by_id(self, id: int) -> None:
        pass


class IJanCodeInfoRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, jancodeinfo: JanCodeInfo):
        pass

    @abstractmethod
    async def find_by_jan_code(self, jan_code: str) -> JanCodeInfo | None:
        pass
