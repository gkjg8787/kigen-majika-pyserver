import pytest

from externalfacade.items import ItemIdentity
from externalfacade import ItemInventory


class TestItemIdentity:
    @pytest.mark.asyncio
    async def test_next_identity_init(self, test_db):
        async def f(db):
            idgenerator = ItemIdentity(db)
            nextid = await idgenerator.next_identity()
            assert int(nextid) >= ItemIdentity.INIT_ID

        async for db in test_db:
            await f(db)

    @pytest.mark.asyncio
    async def test_next_identity_any_id(self, test_db):
        async def f(db):
            id = 2
            iinv = ItemInventory(
                id=id,
                jan_code="0123456789012",
                inventory=0,
                place="",
                expiry_date=None,
            )
            db.add(iinv)
            await db.commit()
            nextid = await ItemIdentity(db).next_identity()
            assert int(nextid) > id

        async for db in test_db:
            await f(db)
