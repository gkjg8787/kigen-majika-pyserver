from datetime import datetime

from pydantic import BaseModel


class ItemComparingData(BaseModel):
    name: str
    jan_code: str
    inventory: int
    place: str
    category: str
    manufacturer: str
    text: str
    expiry_date: datetime | None
