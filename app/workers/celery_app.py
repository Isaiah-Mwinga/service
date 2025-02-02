import os
from celery import Celery

REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "your_password")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")

REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"

celery_app = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)