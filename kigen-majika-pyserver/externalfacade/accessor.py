from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)
import settings

dbconf = settings.DATABASES
is_echo = dbconf["is_echo"]

aengine = create_async_engine(URL.create(**dbconf["default-async"]), echo=is_echo)
aSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=aengine)


async def get_async_session():
    async with aSessionLocal() as ses:
        yield ses
