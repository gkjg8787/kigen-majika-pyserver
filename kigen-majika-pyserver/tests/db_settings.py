import settings

DATABASES = {
    "default": {
        "drivername": "sqlite",
        "database": f"{settings.BASE_DIR}/db/test.sqlite",
    },
    "default-async": {
        "drivername": "sqlite+aiosqlite",
        "database": f"{settings.BASE_DIR}/db/test.sqlite",
    },
    "is_echo": False,
}
