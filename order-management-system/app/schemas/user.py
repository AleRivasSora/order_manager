from sqlmodel import SQLModel, Field
from pydantic import EmailStr, field_validator
from typing import Optional

class UserBase(SQLModel):
    username: str = Field(..., max_length=50, description="Nombre de usuario")
    email: EmailStr = Field(..., description="Correo electrónico del usuario")

    @field_validator("username")
    def validate_username(cls, value):
        if len(value) < 3:
            raise ValueError("El nombre de usuario debe tener al menos 3 caracteres.")
        return value

class UserCreate(UserBase):
    password: str = Field(..., description="Contraseña en texto plano")

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres.")
        return value

class UserRead(UserBase):
    id: int

class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None