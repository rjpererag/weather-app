from ..pipeline.functions import get_transaction_by_id, get_results_by_id

def search_results_func(db_url: str, transaction_id: str) -> dict:
    if not isinstance(transaction_id, str):
        return {"error": "transaction_id must be a string"}

    transaction = get_transaction_by_id(
        db_url=db_url,
        id_=transaction_id
    )

    # TODO: If not transaction
    results = get_results_by_id(
        db_url=db_url,
        pl_id=transaction.results_id
    )

    return results
