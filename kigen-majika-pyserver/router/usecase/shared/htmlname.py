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


class LocalTimeZone:
    JST = "09:00:00"
