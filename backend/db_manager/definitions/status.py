from sqlalchemy import Column, Numeric, String, JSON, TIMESTAMP
from ..config import Base


class Status(Base):

    __tablename__ = "status"

    id = Column(Numeric, primary_key=True, nullable=False)
    status = Column(String(500), nullable=False)

    def __repr__(self):
        return (
            f"Status<(id={self.id}, "
            f"status='{self.status}'>"
        )