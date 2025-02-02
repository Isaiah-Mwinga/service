from app.workers.celery_app import celery_app
import africastalking
import os

# Initialize Africa's Talking
USERNAME = os.getenv("AFRICASTALKING_USERNAME", "your_username")
API_KEY = os.getenv("AFRICASTALKING_API_KEY", "your_api_key")
africastalking.initialize(USERNAME, API_KEY)
sms = africastalking.SMS

@celery_app.task
def send_sms(phone_number: str, message: str):
    """Send an SMS notification to a customer asynchronously"""
    try:
        response = sms.send(message, [phone_number])
        print(f"SMS sent successfully: {response}")
    except Exception as e:
        print(f"Failed to send SMS: {str(e)}")

