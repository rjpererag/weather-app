from celery import Celery


def make_celery(app_name=__name__):
    celery = Celery(
        app_name,
        broker='redis://localhost:6379/0',
        backend='redis://localhost:6379/1'
    )

    celery.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
        task_track_started=True,
        task_time_limit=600,  # 10 minutes max per task
        task_soft_time_limit=540,  # Soft limit at 9 minutes
        broker_connection_retry_on_startup=True,
    )

    return celery


# Create the Celery instance
celery = make_celery('weather_api')