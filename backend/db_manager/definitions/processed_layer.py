from sqlalchemy import Column, String, JSON, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from ..config import Base


class ProcessedLayer(Base):

    __tablename__ = "processed_layer"

    id = Column(String(500), primary_key=True)
    coordinates_id = Column(UUID(as_uuid=True), foreign_key="coordinates_id", nullable=False)
    general_statistics = Column(JSON, nullable=False)
    weather_statistics = Column(JSON, nullable=False)
    precipitation_statistics = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    def __repr__(self):
        return (
            f"ProcessedLayer<(id={self.id}, "
            f"coordinates_id='{self.coordinates_id}', "
            f"general_statistics='{self.general_statistics}', "
            f"weather_statistics='{self.weather_statistics}', "
            f"precipitation_statistics='{self.precipitation_statistics}', "
            f"created_at={self.created_at})>"
        )