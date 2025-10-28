from .db_settings import DBSettings


def create_db_url(settings: DBSettings = DBSettings()) -> str:
    return f"postgresql://{settings.user}:{settings.password}@{settings.host}:{settings.port}/{settings.db_name}"