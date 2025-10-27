from sqlalchemy import Column, String, Numeric, JSON, TIMESTAMP, text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..config import Base


class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(String(500), primary_key=True, default=uuid.uuid4)
    payload = Column(JSON, nullable=False)
    status_id = Column(Numeric, ForeignKey("status.id"), nullable=False)
    results_id = Column(String(500), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    def __repr__(self):
        return (
            f"Transaction<(id={self.id}, "
            f"payload='{self.payload}', "
            f"status_id='{self.status_id}', "
            f"results_id='{self.results_id}', "
            f"created_at={self.created_at})>"
        )