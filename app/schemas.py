from pydantic import BaseModel
from datetime import datetime

class CustomerBase(BaseModel):
    name: str
    code: str

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    item: str
    amount: int
    time: datetime

class OrderCreate(OrderBase):
    customer_id: int

class Order(OrderBase):
    id: int
    customer: Customer
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
