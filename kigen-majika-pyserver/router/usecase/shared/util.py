from datetime import datetime, timezone, tzinfo
from zoneinfo import ZoneInfo


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
