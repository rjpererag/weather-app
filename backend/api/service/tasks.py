from backend.api.service.celery_config import celery
from .pipeline.functions import process_transaction
from .utils import logger

import sys

@celery.task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    name='backend.api.service.tasks.process_weather_transaction'
)
def process_weather_transaction(self, db_url: str, payload: dict):
    logger.info(f"Processing transaction: {payload.get('id')}")
    process = process_transaction(db_url=db_url, payload=payload)
    return process