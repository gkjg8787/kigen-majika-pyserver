from datetime import datetime
from abc import ABCMeta, abstractmethod

from .items import Item, JanCodeInfo


class IItemFactory(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def create(
        cls,
        id: int,
        name: str,
        jan_code: str,
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


class IJanCodeInfoFactory(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def create(
        cls,
        jan_code: str,
        name: str,
        category: str,
        manufacturer: str,
        updated_at: datetime,
    ) -> JanCodeInfo:
        pass
