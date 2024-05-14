from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASES = {
    "default": {
        "drivername": "sqlite",
        "database": f"{BASE_DIR}/db/items.sqlite",
    },
    "default-async": {
        "drivername": "sqlite+aiosqlite",
        "database": f"{BASE_DIR}/db/items.sqlite",
    },
    "is_echo": False,
}
GET_INFO_ONLINE = True
ATTENTION_DISPLAY_FOR_HTML = {
    "DENGEROUS": 0,
    "CAUTION": 30,
    "SOMEWHAT_CAUTION": 183,
}
