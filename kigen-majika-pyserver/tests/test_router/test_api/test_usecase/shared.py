from datetime import datetime

from domain.models import JanCode
from pydantic import BaseModel


class ItemComparingData(BaseModel):
    name: str
    jan_code: JanCode
    inventory: int
    place: str
    category: str
    manufacturer: str
    text: str
    expiry_date: datetime | None
