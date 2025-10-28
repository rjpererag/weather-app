from sqlalchemy.orm import Session
from ..config import DatabaseConfig


class ORM:

    def __init__(self, db_url: str):

        self.db_config = DatabaseConfig(database_url=db_url)

        self.session = None
        self._should_close_session = self.session is None

    def _get_session(self) -> Session:
        """Get the session to use for operations."""
        return self.db_config.get_session()