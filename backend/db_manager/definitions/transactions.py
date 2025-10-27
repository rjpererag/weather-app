from sqlalchemy import Column, String, Numeric, JSON, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from ..config import Base


class ProcessedLayer(Base):

    __tablename__ = "transactions"

    id = Column(String(500), primary_key=True)
    payload = Column(JSON, nullable=False)
    status_id = Column(Numeric, foreign_key="status_id", nullable=False)
    results_id = Column(String(500), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    def __repr__(self):
        return (
            f"Transaction<(id={self.id}, "
            f"payload='{self.payload}', "
            f"status_id='{self.status_id}', "
            f"results_id='{self.results_id}', "
            f"created_at={self.created_at})>"
        )