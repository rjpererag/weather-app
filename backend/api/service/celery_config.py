import os
from celery import Celery

def create_celery_app():
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

    app = Celery(
        'weather_api',
        broker=redis_url,
        backend=redis_url.replace('/0', '/1'),  # Use different DB for backend
    )

    app.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
        task_track_started=True,
        task_time_limit=600,  # 10 minutes max per task
        task_soft_time_limit=540,  # Soft limit at 9 minutes
        broker_connection_retry_on_startup=True,
        include=['backend.api.service.tasks'],
    )
    return app

celery = create_celery_app()


# celery = Celery(
#     'weather_api',
#     broker='redis://localhost:6379/0',
#     backend='redis://localhost:6379/1',
#     include=['backend.api.service.tasks'],
#     task_serializer='json',
#     accept_content=['json'],
#     result_serializer='json',
#     timezone='UTC',
#     enable_utc=True,
#     task_track_started=True,
#     task_time_limit=600,  # 10 minutes max per task
#     task_soft_time_limit=540,  # Soft limit at 9 minutes
#     broker_connection_retry_on_startup=True,
# )