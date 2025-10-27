from typing import Optional
from uuid import UUID

from .orm import ORM
from ..definitions.raw_layer import RawLayer


class RawLayerORM(ORM):
    """Handles all database operations for Coordinates."""

    def __init__(self, db_url: str):
        super().__init__(db_url)

    def create(self, id_, api_response) -> RawLayer:
        session = self._get_session()
        try:
            raw_layer = RawLayer(
                id=id_,
                api_response=api_response
            )
            session.add(raw_layer)
            if self._should_close_session:
                session.commit()
                session.refresh(raw_layer)
            return raw_layer
        except Exception as e:
            if self._should_close_session:
                session.rollback()
            raise e
        finally:
            if self._should_close_session:
                session.close()

    def get_by_id(self, rl_id: UUID) -> Optional[RawLayer]:
        session = self._get_session()
        try:
            return session.query(RawLayer).filter(
                RawLayer.id == rl_id
            ).first()
        finally:
            if self._should_close_session:
                session.close()