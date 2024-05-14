from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    def toDict(self):
        dic = {}
        for col in self.__table__.columns:
            dic[col.name] = getattr(self, col.name)
        return dic


class ItemInventory(Base):
    __tablename__ = "iteminventory"

    id: Mapped[int] = mapped_column(primary_key=True)
    jan_code: Mapped[str]
    inventory: Mapped[int]
    place: Mapped[str] = mapped_column(insert_default="")
    expiry_date: Mapped[datetime] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.CURRENT_TIMESTAMP()
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.CURRENT_TIMESTAMP(),
        onupdate=func.CURRENT_TIMESTAMP(),
        server_onupdate=func.CURRENT_TIMESTAMP(),
    )

    def __repr__(self) -> str:
        return (
            "iteminventory("
            f"id={self.id!r}"
            f", inventory={self.inventory!r}"
            f", place={self.place!r}"
            f", expiry_date={self.expiry_date!r}"
            f", created_at={self.created_at!r}"
            f", updated_at={self.updated_at!r}"
            ")"
        )


class ItemName(Base):
    __tablename__ = "itemname"

    jan_code: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(insert_default="")
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.CURRENT_TIMESTAMP()
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.CURRENT_TIMESTAMP(),
        onupdate=func.CURRENT_TIMESTAMP(),
        server_onupdate=func.CURRENT_TIMESTAMP(),
    )

    def __repr__(self) -> str:
        return (
            "ItemName("
            f"jan_code={self.jan_code!r}"
            f"name={self.name!r}"
            f", created_at={self.created_at!r}"
            f", updated_at={self.updated_at!r}"
            ")"
        )


class ItemCategory(Base):
    __tablename__ = "itemcategory"

    jan_code: Mapped[str] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(insert_default="")
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.CURRENT_TIMESTAMP()
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.CURRENT_TIMESTAMP(),
        onupdate=func.CURRENT_TIMESTAMP(),
        server_onupdate=func.CURRENT_TIMESTAMP(),
    )

    def __repr__(self) -> str:
        return (
            "itemcategory("
            f"jan_code={self.jan_code!r}"
            f", category={self.category!r}"
            f", created_at={self.created_at!r}"
            f", updated_at={self.updated_at!r}"
            ")"
        )


class ItemMemo(Base):
    __tablename__ = "itemmemo"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(insert_default="")
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.CURRENT_TIMESTAMP()
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.CURRENT_TIMESTAMP(),
        onupdate=func.CURRENT_TIMESTAMP(),
        server_onupdate=func.CURRENT_TIMESTAMP(),
    )

    def __repr__(self) -> str:
        return (
            "itemmemo("
            f"id={self.id!r}"
            f", text={self.text!r}"
            f", created_at={self.created_at!r}"
            f", updated_at={self.updated_at!r}"
            ")"
        )


class ItemManufacturer(Base):
    __tablename__ = "itemmanufacturer"

    jan_code: Mapped[str] = mapped_column(primary_key=True)
    manufacturer: Mapped[str] = mapped_column(insert_default="")
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.CURRENT_TIMESTAMP()
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.CURRENT_TIMESTAMP(),
        onupdate=func.CURRENT_TIMESTAMP(),
        server_onupdate=func.CURRENT_TIMESTAMP(),
    )

    def __repr__(self) -> str:
        return (
            "itemmanufacturer("
            f"jan_code={self.jan_code!r}"
            f", manufacturer={self.manufacturer!r}"
            f", created_at={self.created_at!r}"
            f", updated_at={self.updated_at!r}"
            ")"
        )
