from datetime import datetime, timezone, tzinfo
from zoneinfo import ZoneInfo

import settings

JST = ZoneInfo("Asia/Tokyo")


def utcTolocaltime(input_date: datetime, tz: tzinfo):
    if not input_date:
        return None
    if type(input_date) is not datetime:
        return input_date
    if not input_date.tzinfo:
        utc_date = input_date.replace(tzinfo=timezone.utc)
        return utc_date.astimezone(tz)
    return input_date.astimezone(tz)


def toLocalTextFormat(input_date: datetime):
    if not input_date:
        return None
    if type(input_date) is not datetime:
        return input_date
    local_format = "%Y-%m-%d %H:%M:%S"
    return input_date.strftime(local_format)


def toLocalExpiryDateTextFormat(input_date: datetime):
    if not input_date:
        return None
    if type(input_date) is not datetime:
        return input_date
    local_format = "%Y-%m-%d"
    return input_date.strftime(local_format)


def is_expired_for_itemlist_in_html(days: int | None) -> bool:
    if days is None:
        return False
    target = settings.ATTENTION_DISPLAY_FOR_HTML.get("DANGEROUS", None) or 0
    return days <= target


def is_caution_for_itemlist_in_html(days: int | None) -> bool:
    if days is None:
        return False
    target = settings.ATTENTION_DISPLAY_FOR_HTML.get("CAUTION", None) or 30
    return days <= target


def is_somewhat_caution_for_itemlist_in_html(days: int | None) -> bool:
    if days is None:
        return False
    target = settings.ATTENTION_DISPLAY_FOR_HTML.get("SOMEWHAT_CAUTION", None) or 183
    return days <= target
