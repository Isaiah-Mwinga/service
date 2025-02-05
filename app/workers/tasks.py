import os
import africastalking
from app.workers.celery_app import celery

# Load environment variables
USERNAME = os.getenv("AFRICASTALKING_USERNAME", "sandbox")
API_KEY = os.getenv("AFRICASTALKING_API_KEY")

# Ensure API_KEY is set
if not API_KEY:
    raise ValueError("❌ AFRICASTALKING_API_KEY is missing! Make sure it's set in .env")

# Initialize Africa's Talking
africastalking.initialize(USERNAME, API_KEY)
sms = africastalking.SMS

@celery.task(name="app.workers.tasks.send_sms")  # ✅ Explicitly register task
def send_sms(phone_number: str, message: str):
    """Send an SMS notification to a customer asynchronously"""
    try:
        response = sms.send(message, [phone_number])
        print(f"✅ SMS sent successfully: {response}")
        return response
    except Exception as e:
        print(f"❌ Failed to send SMS: {str(e)}")
        return str(e)

# ✅ Ensure Celery auto-imports tasks
celery.autodiscover_tasks(["app.workers"])


