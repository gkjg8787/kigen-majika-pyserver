from abc import ABCMeta, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from model.database import ItemInventory


class IItemIdentity(metaclass=ABCMeta):
    @abstractmethod
    async def next_identity(self) -> str:
        pass


class ItemIdentity(IItemIdentity):
    session: AsyncSession
    INIT_ID = 1

    def __init__(self, session: AsyncSession):
        self.session = session

    async def next_identity(self) -> str:
        db = self.session
        stmt = select(func.max(ItemInventory.id))
        ret = await db.scalar(stmt)
        if ret and int(ret) >= self.INIT_ID:
            return str(ret + 1)
        return str(self.INIT_ID)


class ItemDictIdentity(IItemIdentity):
    database: dict[int, any]
    INIT_ID = 1

    def __init__(self, data: dict):
        self.database = data

    async def next_identity(self) -> str:
        if not self.database:
            return str(self.INIT_ID)
        return str(max(self.database.keys()) + 1)
