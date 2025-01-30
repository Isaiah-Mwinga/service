from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.dependencies import get_current_user
from app.database import SessionLocal

router = APIRouter()

@router.post("/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(SessionLocal), user: dict = Depends(get_current_user)):
    return crud.create_order(db, order)

@router.get("/", response_model=list[schemas.Order])
def read_orders(db: Session = Depends(SessionLocal), user: dict = Depends(get_current_user)):
    return crud.get_orders(db)
