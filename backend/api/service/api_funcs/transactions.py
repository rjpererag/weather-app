from ..pipeline.functions import get_transaction_by_id

def get_transaction_status_func(db_url: str, transaction_id: str) -> dict:

    if not isinstance(transaction_id, str):
        return {"error": "transaction_id must be a string"}

    transaction = get_transaction_by_id(
        db_url=db_url,
        id_=transaction_id
    )

    t_status = str(transaction.status_id)

    if t_status == "0":
        status = "processing"
    elif t_status == "1":
        status = "ready"
    elif t_status == "2":
        status = "failed"
    else:
        status = "unknown"

    return {"status": status}