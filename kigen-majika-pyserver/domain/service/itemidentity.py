from abc import ABCMeta, abstractmethod


class IItemIdentity(metaclass=ABCMeta):
    @abstractmethod
    async def next_identity(self) -> str:
        pass
