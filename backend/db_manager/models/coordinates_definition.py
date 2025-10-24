# database/models/coordinates.py
"""Coordinates model definition."""

import uuid
from sqlalchemy import Column, String, Numeric
from sqlalchemy.dialects.postgresql import UUID
from .config import Base


class Coordinates(Base):
    """Represents a coordinate location in the database."""

    __tablename__ = "coordinates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    city_name = Column(String(500), nullable=False)
    longitude = Column(Numeric, nullable=False)
    latitude = Column(Numeric, nullable=False)

    def __repr__(self):
        return (
            f"<Coordinates(id={self.id}, "
            f"city_name='{self.city_name}', "
            f"lon={self.longitude}, "
            f"lat={self.latitude})>"
        )
