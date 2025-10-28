from typing import Optional
from uuid import UUID

from .orm import ORM
from ..definitions import Transaction, Status

class TransactionsORM(ORM):
    """Handles all database operations for Coordinates."""

    def __init__(self, db_url: str):
        super().__init__(db_url)


    def create(self, payload: dict, status_id) -> Transaction:
        session = self._get_session()
        try:
            transaction = Transaction(
                payload=payload,
                status_id=status_id,
                results_id=payload.get("results_id"),
                raw_layer_id=payload.get("raw_layer_id"),
            )
            session.add(transaction)
            if self._should_close_session:
                session.commit()
                session.refresh(transaction)
            return transaction
        except Exception as e:
            if self._should_close_session:
                session.rollback()
            raise e
        finally:
            if self._should_close_session:
                session.close()

    def get_by_id(self, t_id: UUID) -> Optional[Transaction]:
        session = self._get_session()
        try:
            return session.query(Transaction).filter(
                Transaction.id == t_id
            ).first()
        finally:
            if self._should_close_session:
                session.close()


    def get_results_id(self, results_id: UUID) -> Optional[Transaction]:
        """Get a processed layer id that maps to the processed data"""
        session = self._get_session()
        try:
            return session.query(Transaction).filter(
                Transaction.results_id == results_id
            ).first()
        finally:
            if self._should_close_session:
                session.close()


    def update_status_id(self, t_id: UUID | str, new_status_id: int) -> Optional[Transaction]:
        """Get a processed layer id that maps to the processed data"""
        session = self._get_session()
        try:
            transaction = session.query(Transaction).filter(
                Transaction.id == t_id
            ).first()

            if not transaction:
                raise ValueError(f"Transaction {t_id} not found")

            transaction.status_id = new_status_id

            session.commit()
            session.refresh(transaction)
            return transaction

        except Exception as e:
            if self._should_close_session:
                session.rollback()
                raise e

        finally:
            if self._should_close_session:
                session.close()