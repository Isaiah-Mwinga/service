from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.dependencies import get_db, get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.Customer)
async def create_customer(
    customer: schemas.CustomerCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)  # Require OpenID authentication
):
    """Create a new customer (requires OpenID authentication)"""
    return crud.create_customer(db, customer)

@router.get("/", response_model=list[schemas.Customer])
async def read_customers(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)  # Require OpenID authentication
):
    """Retrieve all customers (requires OpenID authentication)"""
    return crud.get_customers(db)