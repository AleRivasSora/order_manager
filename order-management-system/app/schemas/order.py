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
    item_id: int = Field(..., description="ID del producto")
    quantity: int = Field(..., gt=0, description="Cantidad del producto")

    @field_validator("quantity")
    def validate_quantity(cls, value):
        if value <= 0:
            raise ValueError("La cantidad debe ser mayor a 0.")
        return value

class OrderBase(SQLModel):
    customer_id: int = Field(..., description="ID del cliente que realizó la orden")
    employee_id: Optional[int] = Field(None, description="ID del empleado asignado")
    status: OrderStatus = Field(default=OrderStatus.pending, description="Estado de la orden")
    items: List[OrderItem] = Field(..., description="Lista de productos en la orden")

    @field_validator("status")
    def validate_status(cls, value):
        if value not in OrderStatus.__members__.values():
            raise ValueError("El estado de la orden no es válido.")
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