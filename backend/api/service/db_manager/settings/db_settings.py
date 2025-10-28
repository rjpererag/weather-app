from dataclasses import dataclass
from decouple import config


@dataclass
class DBSettings:
    user: str = config("POSTGRES_USER")
    db_name: str = config("POSTGRES_DB")
    host: str = config("POSTGRES_HOST")
    port: str = config("POSTGRES_PORT")
    password: str = config("POSTGRES_PASSWORD")