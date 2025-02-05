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







# import os
# from celery import Celery
# from dotenv import load_dotenv

# # Load environment variables
# dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
# load_dotenv(dotenv_path)

# # Redis configuration
# REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "your_password")
# REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
# REDIS_PORT = os.getenv("REDIS_PORT", "6379")

# # REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"
# REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


# # Initialize Celery
# celery_app = Celery(
#     "worker",
#     broker=REDIS_URL,
#     backend=REDIS_URL,
# )

# # Ensure Celery finds all tasks automatically
# celery_app.autodiscover_tasks(["app.workers"])
