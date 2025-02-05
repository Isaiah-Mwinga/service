from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CustomerBase(BaseModel):
    name: str
    code: str
    phone_number: str

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int

    class Config:
        from_attributes = True

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    phone_number: Optional[str] = None  # Add phone_number field

class OrderBase(BaseModel):
    item: str
    amount: int
    time: datetime

class OrderCreate(OrderBase):
    customer_id: int

class Order(OrderBase):
    id: int
    customer_id: int

    class Config:
        from_attributes = True

class OrderUpdate(BaseModel):
    item: Optional[str] = None
    amount: Optional[float] = None
