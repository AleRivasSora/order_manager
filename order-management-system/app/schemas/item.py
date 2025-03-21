from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import field_validator

class ItemBase(SQLModel):
    name: str = Field(..., max_length=100, description="Nombre del producto")
    description: Optional[str] = Field(None, description="Descripción del producto")
    price: float = Field(..., gt=0, description="Precio del producto")
    stock: int = Field(..., ge=0, description="Cantidad disponible en inventario")

    @field_validator("price")
    def validate_price(cls, value):
        if value <= 0:
            raise ValueError("El precio debe ser mayor a 0.")
        return value

class ItemCreate(ItemBase):
    pass

class ItemRead(ItemBase):
    id: int

class ItemUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None