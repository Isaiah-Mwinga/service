from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.dependencies import get_db
from app.workers.tasks import send_sms  # Import Celery task

router = APIRouter()


@router.post("/", response_model=schemas.Order)
async def create_order(
    order: schemas.OrderCreate, db: Session = Depends(get_db)
):
    """Create an order and send an SMS notification (No authentication required)"""
    new_order = crud.create_order(db, order)

    # Fetch the customer's phone number (assuming it's stored in the DB)
    customer = (
        db.query(crud.models.Customer).filter_by(id=order.customer_id).first()
    )
    if customer and hasattr(
        customer, "phone_number"
    ):  # Ensure phone number exists
        message = f"Hello {customer.name}, your order for {order.item} has been received. Amount: ${order.amount}."
        send_sms.delay(
            customer.phone_number, message
        )  # Send SMS asynchronously

    return new_order


@router.get("/", response_model=list[schemas.Order])
async def get_orders(db: Session = Depends(get_db)):
    """Retrieve all orders"""
    return crud.get_orders(db)


@router.get("/{order_id}", response_model=schemas.Order)
async def get_order(order_id: int, db: Session = Depends(get_db)):
    """Retrieve a single order by ID"""
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/{order_id}", response_model=schemas.Order)
async def update_order(
    order_id: int,
    order_update: schemas.OrderUpdate,
    db: Session = Depends(get_db),
):
    """Update an existing order"""
    order = crud.update_order(db, order_id, order_update)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.delete("/{order_id}")
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    """Delete an order"""
    deleted = crud.delete_order(db, order_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}
