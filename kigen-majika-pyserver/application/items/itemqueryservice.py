from abc import ABCMeta, abstractmethod

from pydantic import BaseModel


from domain.models import Item


class ItemQueryCommand(BaseModel):
    isort: int
    stock: int
    stype: int
    word: str


class ItemQueryResult(BaseModel):
    items: list[Item] = []


class IItemQueryService(metaclass=ABCMeta):
    @abstractmethod
    async def find_all(self, itemquerycommand: ItemQueryCommand) -> ItemQueryResult:
        pass
