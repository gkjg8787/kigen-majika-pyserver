from datetime import datetime, timezone

from model.domain import Item, ItemFactory


def get_item(
    id: int = 1,
    name: str = "test",
    jan_code: str = "0123456789012",
    inventory: int = 1,
    place: str = "closet",
    category: str = "any",
    manufacturer: str = "maker",
    text: str = "memo",
    expiry_date: datetime | None = None,
    created_at: datetime | None = None,
    updated_at: datetime | None = None,
) -> Item:
    now = datetime.now(timezone.utc)
    if created_at is None:
        created_at = now
    if updated_at is None:
        updated_at = now
    return ItemFactory.create(
        id=id,
        name=name,
        jan_code=jan_code,
        inventory=inventory,
        place=place,
        category=category,
        manufacturer=manufacturer,
        text=text,
        expiry_date=expiry_date,
        created_at=created_at,
        updated_at=updated_at,
    )
