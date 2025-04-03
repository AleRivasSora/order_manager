from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import field_validator

class ItemBase(SQLModel):
    name: str = Field(..., max_length=100, description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., gt=0, description="Product price")
    stock: int = Field(..., ge=0, description="Available stock in inventory")

    @field_validator("price")
    def validate_price(cls, value):
        if value <= 0:
            raise ValueError("The price must be greater than 0.")
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