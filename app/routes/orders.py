from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.dependencies import get_db, get_current_user
from app.workers.tasks import send_sms  # Import Celery task

router = APIRouter()

@router.post("/", response_model=schemas.Order)
async def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """Create an order and send an SMS notification"""
    new_order = crud.create_order(db, order)

    # Fetch the customer's phone number (assuming it's stored in the DB)
    customer = db.query(crud.models.Customer).filter_by(id=order.customer_id).first()
    if customer and hasattr(customer, "phone_number"):  # Ensure phone number exists
        message = f"Hello {customer.name}, your order for {order.item} has been received. Amount: ${order.amount}."
        send_sms.delay(customer.phone_number, message)  # Send SMS asynchronously

    return new_order

