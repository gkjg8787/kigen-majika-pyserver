from datetime import datetime, timezone

from domain.models import Item
from externalfacade.items import ItemFactory, JanCodeFactory


def get_item(
    id: int,
    name: str = "",
    expiry_date: datetime | None = None,
    created_at: datetime | None = None,
    updated_at: datetime | None = None,
):
    if not name:
        name = f"test{id}"
    now = datetime.now(timezone.utc)
    if not created_at:
        created_at = now
    if not updated_at:
        updated_at = now
    return ItemFactory.create(
        id=id,
        name=name,
        jan_code=JanCodeFactory.create(jan_code=str(id)),
        inventory=1,
        place="",
        category="",
        manufacturer="",
        text="",
        expiry_date=expiry_date,
        created_at=created_at,
        updated_at=updated_at,
    )
