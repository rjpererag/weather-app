from sqlalchemy import Column, String, Numeric, JSON, TIMESTAMP, text, ForeignKey
import uuid
from ..config import Base


class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(String(500), primary_key=True, default=uuid.uuid4)
    payload = Column(JSON, nullable=False)
    status_id = Column(Numeric, ForeignKey("status.id"), nullable=False)
    results_id = Column(String(500), nullable=False)
    raw_layer_id = Column(String(500), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    def __repr__(self):
        return (
            f"Transaction<(id={self.id}, "
            f"payload='{self.payload}', "
            f"status_id='{self.status_id}', "
            f"results_id='{self.results_id}', "
            f"raw_layer_id='{self.raw_layer_id}', "
            f"created_at={self.created_at})>"
        )

    def to_dict(self):
        return {
            "id": str(self.id),
            "payload": self.payload,
            "status_id": float(self.status_id) if self.status_id is not None else None,
            "results_id": self.results_id,
            "raw_layer_id": self.raw_layer_id,
            "created_at": str(self.created_at)
        }