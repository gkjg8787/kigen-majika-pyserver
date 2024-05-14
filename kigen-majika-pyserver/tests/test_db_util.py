import sys
import os
import argparse
from enum import Enum
import asyncio

from os.path import dirname

from sqlalchemy import URL
from sqlalchemy_utils import (
    database_exists,
)
from sqlalchemy.ext.asyncio import (
    create_async_engine,
)

from tests.db_settings import DATABASES
from externalfacade.items.items import Base

parent_dir = dirname(dirname(__file__))
sys.path.append(parent_dir)


TEST_DB_URL = URL.create(**DATABASES["default-async"])
is_echo = DATABASES["is_echo"]
engine = create_async_engine(TEST_DB_URL, echo=is_echo)


def create_database():
    if "sqlite" in DATABASES["default-async"]["drivername"]:
        return

    async def create_database_func(dbkey):
        engine_url = URL.create(**DATABASES[dbkey])
        if database_exists(engine_url):
            return
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(create_database_func("default-sync"))


def drop_database():
    if "sqlite" in DATABASES["default-async"]["drivername"]:
        os.remove(DATABASES["default-async"]["database"])
        return

    async def drop_database_func(dbkey):
        engine_url = URL.create(**DATABASES[dbkey])
        if not database_exists(engine_url):
            return
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    asyncio.run(drop_database_func("default-async"))


class DBCommandName(Enum):
    CREATE = "create"
    DROP = "drop"
    RECREATE = "recreate"


def parse_paramter(argv):
    parser = argparse.ArgumentParser(description="table create and drop")
    parser.add_argument("name", type=str, choices=[v.value for v in DBCommandName])

    args = parser.parse_args(argv[1:])
    return args


def main(argv):
    param = parse_paramter(argv)
    if param.name == DBCommandName.RECREATE.value:
        drop_database()
        create_database()
        return
    if param.name == DBCommandName.CREATE.value:
        create_database()
        return
    if param.name == DBCommandName.DROP.value:
        drop_database()
        return
    return


if __name__ == "__main__":
    main(sys.argv)
