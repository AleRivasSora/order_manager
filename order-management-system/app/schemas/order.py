from sqlmodel import SQLModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime
from pydantic import field_validator

class OrderStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"

class OrderItem(SQLModel):
    item_id: int = Field(..., description="Product ID")
    quantity: int = Field(..., gt=0, description="Quantity of the product")

    @field_validator("quantity")
    def validate_quantity(cls, value):
        if value <= 0:
            raise ValueError("The quantity must be greater than 0.")
        return value

class OrderBase(SQLModel):
    customer_id: int = Field(..., description="ID of the customer who placed the order")
    employee_id: Optional[int] = Field(None, description="ID of the assigned employee")
    status: OrderStatus = Field(default=OrderStatus.pending, description="Order status")
    items: List[OrderItem] = Field(..., description="List of products in the order")

    @field_validator("status")
    def validate_status(cls, value):
        if value not in OrderStatus.__members__.values():
            raise ValueError("The order status is not valid.")
        return value

class OrderCreate(OrderBase):
    pass

class OrderRead(OrderBase):
    id: int
    created_at: datetime
    updated_at: datetime

class OrderUpdate(SQLModel):
    status: Optional[OrderStatus] = None
    employee_id: Optional[int] = None
    items: Optional[List[OrderItem]] = None