from fastapi import HTTPException
from typing import List
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderUpdate, OrderRead
from sqlalchemy.orm import Session
from datetime import datetime

class OrderController:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, order: OrderCreate) -> OrderRead:
        try:
            # Convert OrderCreate schema to Order model
            db_order = Order(**order.dict())
            self.db.add(db_order)
            self.db.commit()
            self.db.refresh(db_order)
            return OrderRead.from_orm(db_order)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error creating order: {str(e)}")

    def get_order(self, order_id: int) -> OrderRead:
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return OrderRead.from_orm(order)

    def update_order(self, order_id: int, order_update: OrderUpdate) -> OrderRead:
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        try:
            # Update only the fields provided in the OrderUpdate schema
            update_data = order_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(order, key, value)
            order.updated_at = datetime.now()  # Update the timestamp
            self.db.commit()
            self.db.refresh(order)
            return OrderRead.from_orm(order)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error updating order: {str(e)}")

    def get_all_orders(self) -> List[OrderRead]:
        try:
            orders = self.db.query(Order).all()
            return [OrderRead.from_orm(order) for order in orders]
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error retrieving orders: {str(e)}")