from datetime import datetime
from abc import ABCMeta, abstractmethod

from .items import Item, JanCodeInfo, JanCode


class IItemFactory(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def create(
        cls,
        id: int,
        name: str,
        jan_code: JanCode,
        inventory: int,
        place: str,
        category: str,
        manufacturer: str,
        text: str,
        expiry_date: datetime,
        created_at: datetime,
        updated_at: datetime,
    ) -> Item:
        pass


class IJanCodeFactory(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def create(cls, jan_code: str) -> JanCode:
        pass


class IJanCodeInfoFactory(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def create(
        cls,
        jan_code: JanCode,
        name: str,
        category: str,
        manufacturer: str,
        updated_at: datetime,
    ) -> JanCodeInfo:
        pass
