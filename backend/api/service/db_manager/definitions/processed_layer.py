from sqlalchemy import Column, String, JSON, TIMESTAMP, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from ..config import Base
from ..definitions import Coordinates, RawLayer


class ProcessedLayer(Base):

    __tablename__ = "processed_layer"

    id = Column(String(500), primary_key=True)
    raw_layer_id = Column(String(500), ForeignKey("raw_layer.id"), nullable=False)
    general_statistics = Column(JSON, nullable=False)
    weather_statistics = Column(JSON, nullable=False)
    precipitation_statistics = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    def __repr__(self):
        return (
            f"ProcessedLayer<(id={self.id}, "
            f"general_statistics='{self.general_statistics}', "
            f"weather_statistics='{self.weather_statistics}', "
            f"precipitation_statistics='{self.precipitation_statistics}', "
            f"created_at={self.created_at})>"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "general_statistics": self.general_statistics,
            "weather_statistics": self.weather_statistics,
            "precipitation_statistics": self.precipitation_statistics,
            "created_at": str(self.created_at),
        }