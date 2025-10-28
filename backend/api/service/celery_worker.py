from backend.api.service.celery_config import celery
from backend.api.service import tasks

__all__ = ["celery"]
if __name__ == "__main__":
    celery.start()