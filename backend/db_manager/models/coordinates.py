from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from .orm import ORM
from ..definitions.coordinates import Coordinates


class CoordinatesORM(ORM):
    """Handles all database operations for Coordinates."""

    def __init__(self, db_url: str):
        super().__init__(db_url)

    def create(self, city_name: str, longitude: float, latitude: float) -> Coordinates:
        session = self._get_session()
        try:
            coordinate = Coordinates(
                city_name=city_name,
                longitude=longitude,
                latitude=latitude
            )
            session.add(coordinate)
            if self._should_close_session:
                session.commit()
                session.refresh(coordinate)
            return coordinate
        except Exception as e:
            if self._should_close_session:
                session.rollback()
            raise e
        finally:
            if self._should_close_session:
                session.close()

    def get_by_id(self, coord_id: UUID) -> Optional[Coordinates]:
        session = self._get_session()
        try:
            return session.query(Coordinates).filter(
                Coordinates.id == coord_id
            ).first()
        finally:
            if self._should_close_session:
                session.close()

    def get_by_city_name(self, city_name: str) -> Optional[Coordinates]:
        session = self._get_session()
        try:
            return session.query(Coordinates).filter(
                Coordinates.city_name == city_name
            ).first()
        finally:
            if self._should_close_session:
                session.close()

    def get_all(self, limit: int = None, offset: int = 0) -> List[Coordinates]:
        session = self._get_session()
        try:
            query = session.query(Coordinates)
            if limit:
                query = query.limit(limit).offset(offset)
            return query.all()
        finally:
            if self._should_close_session:
                session.close()


    def update(
            self,
            coord_id: UUID,
            city_name: str = None,
            longitude: float = None,
            latitude: float = None
    ) -> Optional[Coordinates]:

        session = self._get_session()
        try:
            coordinate = session.query(Coordinates).filter(
                Coordinates.id == coord_id
            ).first()

            if not coordinate:
                return None

            if city_name is not None:
                coordinate.city_name = city_name
            if longitude is not None:
                coordinate.longitude = longitude
            if latitude is not None:
                coordinate.latitude = latitude

            if self._should_close_session:
                session.commit()
                session.refresh(coordinate)

            return coordinate
        except Exception as e:
            if self._should_close_session:
                session.rollback()
            raise e
        finally:
            if self._should_close_session:
                session.close()

    def delete(self, coord_id: UUID) -> bool:
        session = self._get_session()
        try:
            coordinate = session.query(Coordinates).filter(
                Coordinates.id == coord_id
            ).first()

            if not coordinate:
                return False

            session.delete(coordinate)
            if self._should_close_session:
                session.commit()

            return True
        except Exception as e:
            if self._should_close_session:
                session.rollback()
            raise e
        finally:
            if self._should_close_session:
                session.close()

    def count(self) -> int:
        session = self._get_session()
        try:
            return session.query(Coordinates).count()
        finally:
            if self._should_close_session:
                session.close()