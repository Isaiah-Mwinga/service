from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.dependencies import get_db
from app.routes.auth import get_current_user

router = APIRouter()


@router.post("/", response_model=schemas.Customer)
async def create_customer(
    customer: schemas.CustomerCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),  # 🔒 Requires authentication
):
    return crud.create_customer(db, customer)


@router.get("/", response_model=list[schemas.Customer])
async def read_customers(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),  # 🔒 Requires authentication
):
    return crud.get_customers(db)


@router.get("/{customer_id}", response_model=schemas.Customer)
async def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),  # 🔒 Requires authentication
):
    customer = crud.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.put("/{customer_id}", response_model=schemas.Customer)
async def update_customer(
    customer_id: int,
    customer_update: schemas.CustomerUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),  # 🔒 Requires authentication
):
    customer = crud.update_customer(db, customer_id, customer_update)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.delete("/{customer_id}")
async def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),  # 🔒 Requires authentication
):
    deleted = crud.delete_customer(db, customer_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted successfully"}
