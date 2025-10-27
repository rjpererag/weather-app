from sqlalchemy import Column, String, JSON, TIMESTAMP
from ..config import Base


class RawLayer(Base):

    __tablename__ = "raw_layer"

    id = Column(String(500), primary_key=True)
    api_response = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    def __repr__(self):
        return (
            f"RawLayer<(id={self.id}, "
            f"api_response='{self.api_response}', "
            f"created_at={self.created_at})>"
        )