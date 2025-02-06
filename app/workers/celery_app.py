import os
from celery import Celery

REDIS_URL = os.getenv("CELERY_BROKER_URL", "redis://:your_password@localhost:6379/0")

celery = Celery("worker", 
                broker=REDIS_URL,
                backend=REDIS_URL,
                include=["app.workers.tasks"],
                )

celery.autodiscover_tasks(["app.workers"])

@celery.task
def send_sms(phone, message):
    print(f"📨 Sending SMS to {phone}: {message}")
    return f"Message sent to {phone}"

