from datetime import datetime, timezone
from slugify import slugify


def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)


def generate_slug_from_name(data: dict) -> dict:
    if not data.get("slug") and data.get("name"):
        data["slug"] = slugify(data["name"])
    return data
