from celery_config import celery
from .pipeline.functions import process_transaction


@celery.task(bind=True, max_retries=3, default_retry_delay=60)
def process_weather_transaction(db_url: str, payload: dict):
    return process_transaction(db_url=db_url, payload=payload)