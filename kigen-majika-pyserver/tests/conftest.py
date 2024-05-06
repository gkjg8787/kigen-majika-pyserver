import pytest

from sqlalchemy import URL, create_engine
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)

from main import app
from tests.db_settings import DATABASES
from model.database.items import Base
from model.database import get_async_session


@pytest.fixture(scope="session")
async def test_db():
    TEST_DB_URL = URL.create(**DATABASES["default-async"])
    is_echo = DATABASES["is_echo"]
    async_engine = create_async_engine(TEST_DB_URL, echo=is_echo)
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    TestingSessionLocal = async_sessionmaker(
        autocommit=False, autoflush=False, bind=async_engine
    )

    async def get_db_for_testing():
        async with TestingSessionLocal() as ses:
            yield ses

    # 　テスト時に依存するDBを本番用からテスト用のものに切り替える
    app.dependency_overrides[get_async_session] = get_db_for_testing
    async with TestingSessionLocal() as ses:
        yield ses

    await async_engine.dispose()
