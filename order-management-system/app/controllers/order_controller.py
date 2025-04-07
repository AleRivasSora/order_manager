from fastapi import HTTPException
from typing import List
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderUpdate, OrderRead
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime


class OrderController:
    def __init__(self, db: Session):
        self.db = db

    def _get_order_by_id(self, order_id: int) -> Order:
        """
        Helper method to retrieve an order by ID.
        Raises an HTTPException if the order is not found.
        """
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order

    def create_order(self, order: OrderCreate) -> OrderRead:
        """
        Creates a new order in the database.
        """
        try:
            db_order = Order(**order.dict())
            self.db.add(db_order)
            self.db.commit()
            self.db.refresh(db_order)
            return OrderRead.from_orm(db_order)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Error creating order: Integrity constraint violated.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    def get_order(self, order_id: int) -> OrderRead:
        """
        Retrieves an order by ID.
        """
        order = self._get_order_by_id(order_id)
        return OrderRead.from_orm(order)

    def update_order(self, order_id: int, order_update: OrderUpdate) -> OrderRead:
        """
        Updates an existing order.
        """
        order = self._get_order_by_id(order_id)
        try:
            update_data = order_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(order, key, value)
            order.updated_at = datetime.now()  # Update the timestamp
            self.db.commit()
            self.db.refresh(order)
            return OrderRead.from_orm(order)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Error updating order: Integrity constraint violated.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    def get_all_orders(self, skip: int = 0, limit: int = 10) -> List[OrderRead]:
        """
        Retrieves all orders with pagination.
        """
        try:
            orders = self.db.query(Order).offset(skip).limit(limit).all()
            return [OrderRead.from_orm(order) for order in orders]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving orders: {str(e)}")