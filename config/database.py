import os

from dotenv import load_dotenv

load_dotenv()

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "database": os.getenv("POSTGRES_DB"),
                "user": os.getenv("POSTGRES_USER"),
                "password": os.getenv("POSTGRES_PASSWORD"),
                "host": os.getenv("POSTGRES_HOST"),
            },
        }
    },
    "apps": {
        "models": {"models": ["wallet.models", "users.models"], "default_connection": "default"},
        "aerich": {"models": ["aerich.models"], "default_connection": "default"},
    },
}
