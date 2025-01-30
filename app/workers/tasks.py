from app.workers.celery_app import celery_app
import africastalking
import time

africastalking.initialize("sandbox", "api_key")
sms = africastalking.SMS

@celery_app.task
async def send_sms(phone_number: str, message: str):
    await time.sleep(2)  # Simulate async processing
    sms.send(message, [phone_number])
