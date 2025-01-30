from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.dependencies import get_current_user
from app.database import SessionLocal

router = APIRouter()

@router.post("/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(SessionLocal), user: dict = Depends(get_current_user)):
    return crud.create_customer(db, customer)

@router.get("/", response_model=list[schemas.Customer])
def read_customers(db: Session = Depends(SessionLocal), user: dict = Depends(get_current_user)):
    return crud.get_customers(db)
