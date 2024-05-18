from enum import Enum, auto


class AutoLowerName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()


class POSTNAME(AutoLowerName):
    ID = auto()
    NAME = auto()
    JAN_CODE = auto()
    INVENTORY = auto()
    PLACE = auto()
    CATEGORY = auto()
    MANUFACTURER = auto()
    TEXT = auto()
    EXPIRY_DATE = auto()
    LOCAL_TIMEZONE = auto()


class GETNAME(AutoLowerName):
    ISORT = auto()
    STOCK = auto()
    STYPE = auto()
    WORD = auto()


class LocalTimeZone:
    JST = "09:00:00"


class FORMMETHOD(AutoLowerName):
    GET = auto()
    POST = auto()


class HTMLTemplateValue:
    SELECTED = "selected"
    CHECKED = "checked"


class HTMLViewError(Enum):
    NOT_RESULT_API = (1, "情報の取得に失敗しました")

    def __init__(self, id: int, text: str):
        self.id = id
        self.ename = self.name.lower()
        self.jname = text
