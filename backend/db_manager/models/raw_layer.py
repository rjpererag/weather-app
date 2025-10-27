from typing import List, Optional
from uuid import UUID

from .orm import ORM
from ..definitions.raw_layer import RawLayer


class RawLayerORM(ORM):
    """Handles all database operations for Coordinates."""

    def __init__(self, db_url: str):
        super().__init__(db_url)

    @staticmethod
    def _create_id(longitude: float, latitude: float, start_date: str, end_date: str) -> str:
        return f"rl-{longitude}-{latitude}-{start_date}-{end_date}"

    def create(self, longitude: float, latitude: float, start_date: str, end_date: str) -> RawLayer:
        session = self._get_session()

    def get_by_id(self, rl_id: UUID) -> Optional[RawLayer]:
        session = self._get_session()
        try:
            return session.query(RawLayer).filter(
                RawLayer.id == rl_id
            ).first()
        finally:
            if self._should_close_session:
                session.close()