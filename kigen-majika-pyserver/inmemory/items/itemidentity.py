from domain.service import IItemIdentity


class ItemDictIdentity(IItemIdentity):
    database: dict[int, any]
    INIT_ID = 1

    def __init__(self, data: dict):
        self.database = data

    async def next_identity(self) -> str:
        if not self.database:
            return str(self.INIT_ID)
        return str(max(self.database.keys()) + 1)
