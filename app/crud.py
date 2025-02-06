from sqlalchemy.orm import Session
from app import models, schemas


def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.model_dump())  # ✅ Fix here
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def get_customers(db: Session):
    return db.query(models.Customer).all()


def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()


def update_customer(
    db: Session, customer_id: int, customer_update: schemas.CustomerUpdate
):
    customer = get_customer(db, customer_id)
    if not customer:
        return None
    for key, value in customer_update.model_dump(
        exclude_unset=True
    ).items():  # ✅ Fix here
        setattr(customer, key, value)
    db.commit()
    db.refresh(customer)
    return customer


def delete_customer(db: Session, customer_id: int):
    customer = get_customer(db, customer_id)
    if not customer:
        return False
    db.delete(customer)
    db.commit()
    return True


def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(**order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_orders(db: Session):
    return db.query(models.Order).all()


def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def update_order(db: Session, order_id: int, order_update: schemas.OrderUpdate):
    order = get_order(db, order_id)
    if not order:
        return None
    for key, value in order_update.model_dump(exclude_unset=True).items():
        setattr(order, key, value)
    db.commit()
    db.refresh(order)
    return order


def delete_order(db: Session, order_id: int):
    order = get_order(db, order_id)
    if not order:
        return False
    db.delete(order)
    db.commit()
    return True
