from datetime import datetime

from enum import Enum
from pydantic import BaseModel, field_validator


class JanCode(BaseModel):
    value: str

    @field_validator("value")
    @classmethod
    def to_half_width_str(cls, v):
        try:
            vv = int(v)
        except ValueError as err:
            raise ValueError("cannot convert to int")
        if vv < 0:
            raise ValueError("less than 0")
        return str(vv).zfill(len(v))


class JanCodeInfo(BaseModel):
    jan_code: JanCode
    name: str
    category: str
    manufacturer: str
    updated_at: datetime


class Item(BaseModel):
    id: int
    name: str = ""
    jan_code: JanCode
    inventory: int = 0
    place: str = ""
    category: str = ""
    manufacturer: str = ""
    text: str = ""
    expiry_date: datetime | None = None
    created_at: datetime
    updated_at: datetime

    @field_validator("inventory")
    @classmethod
    def inventory_out_of_range(cls, v):
        try:
            vv = int(v)
        except ValueError as err:
            raise ValueError("cannot convert to int")
        if vv < 0:
            raise ValueError("less than 0")
        return v


class ItemSort(Enum):
    NEAR_EXPIRY = (1, "消費期限が近い")
    FAR_EXPIRY = (2, "消費期限が遠い")
    OLD_REGIST = (3, "登録が古い")
    NEW_REGIST = (4, "登録が新しい")
    ITEMNAME_ASC = (5, "商品名昇")
    ITEMNAME_DESC = (6, "商品名降")

    def __init__(self, id: int, text: str):
        self.id = id
        self.ename = self.name.lower()
        self.jname = text


class ItemStockFilter(Enum):
    ALL = (1, "全て")
    IN_STOCK = (2, "在庫あり")
    NO_STOCK = (3, "在庫なし")

    def __init__(self, id: int, text: str):
        self.id = id
        self.ename = self.name.lower()
        self.jname = text


class ItemSearchType(Enum):
    NAME = (1, "商品名")
    JANCODE = (2, "JANコード")
    CATEGORY = (3, "カテゴリー")
    MANUFACTURER = (4, "メーカー")
    PLACE = (5, "保管場所")
    MEMO = (6, "備考")

    def __init__(self, id: int, text: str):
        self.id = id
        self.ename = self.name.lower()
        self.jname = text
