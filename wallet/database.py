import os

from dotenv import load_dotenv

load_dotenv()

_user = os.getenv('POSTGRES_USER')
_password = os.getenv('POSTGRES_PASSWORD')
_host = os.getenv('POSTGRES_HOST')
_port = os.getenv('POSTGRES_PORT')
_db_name = os.getenv('POSTGRES_WALLET_NAME')

DATABASE_URL = f"postgres://{_user}:{_password}@{_host}:{_port}/{_db_name}"


DATABASE_CONFIG = {
    "connections": {
        "default": DATABASE_URL
    },
    "apps": {
        "wallet": {
            "models": ["aerich.models", "wallet.models"],
            "default_connection": "default"
        },
        "users": {
            "models": ["aerich.models", "users.models"],
            "default_connection": "default"
        }
    }
}
