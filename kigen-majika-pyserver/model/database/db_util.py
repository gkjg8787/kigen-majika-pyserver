from sqlalchemy import URL, create_engine

from settings import DATABASES
from model.database import items

dbconf = DATABASES
url_obj = URL.create(**dbconf["default"])
is_echo = dbconf["is_echo"]
engine = create_engine(url_obj, echo=is_echo)


def create_db():
    items.Base.metadata.create_all(engine)


def remove_db():
    items.Base.metadata.drop_all(engine)
