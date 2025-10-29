from ..pipeline.functions import generate_ids, create_new_transaction
from ..tasks import process_weather_transaction


def post_weather_data_func(
        db_url: str,
        latitude: str,
        longitude: str,
        start_date: str,
        end_date: str
) -> dict:

    payload = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date
    }

    ids = generate_ids(payload=payload)
    payload = {**payload, **ids}

    transaction = create_new_transaction(db_url=db_url, payload=payload)

    if not transaction:
        return {"error": "bad request, no transaction created"}

    payload = {**payload, **transaction}
    task = process_weather_transaction.delay(db_url, payload)

    return transaction
