from sqlmodel import SQLModel, Field
from pydantic import EmailStr, field_validator
from typing import Optional

class UserBase(SQLModel):
    username: str = Field(..., max_length=50, description="Username")
    email: EmailStr = Field(..., description="User's email address")

    @field_validator("username")
    def validate_username(cls, value):
        if len(value) < 3:
            raise ValueError("The username must be at least 3 characters long.")
        return value

class UserCreate(UserBase):
    password: str = Field(..., description="Plain text password")

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("The password must be at least 8 characters long.")
        return value

class UserRead(UserBase):
    id: int

class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None