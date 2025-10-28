from typing import Optional
from uuid import UUID

from .orm import ORM
from ..definitions.processed_layer import ProcessedLayer
from backend.utils import StatisticsGenerator

class ProcessedLayerORM(ORM):
    """Handles all database operations for Coordinates."""

    def __init__(self, db_url: str):
        super().__init__(db_url)
        self.stats_generator = StatisticsGenerator()


    def create(self, payload: dict) -> ProcessedLayer:
        session = self._get_session()


        try:
            processed_layer = ProcessedLayer(
                id=payload.get("results_id"),
                raw_layer_id=payload.get("raw_layer_id"),
                coordinates_id=payload.get("coordinates_id"),
                general_statistics=payload.get("general_stats"),
                weather_statistics=payload.get("weather_stats"),
                precipitation_statistics=payload.get("precipitation_stats"),
            )
            session.add(processed_layer)
            if self._should_close_session:
                session.commit()
                session.refresh(processed_layer)
            return processed_layer
        except Exception as e:
            if self._should_close_session:
                session.rollback()
            raise e
        finally:
            if self._should_close_session:
                session.close()

    def get_by_id(self, pl_id: UUID) -> Optional[ProcessedLayer]:
        session = self._get_session()
        try:
            return session.query(ProcessedLayer).filter(
                ProcessedLayer.id == pl_id
            ).first()
        finally:
            if self._should_close_session:
                session.close()