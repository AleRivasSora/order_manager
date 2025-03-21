from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import field_validator

class EmployeeBase(SQLModel):
    name: str = Field(..., max_length=100, description="Nombre del empleado")
    role: str = Field(..., description="Rol del empleado (ejemplo: 'chef', 'waiter')")

    @field_validator("role")
    def validate_role(cls, value):
        allowed_roles = ["chef", "waiter", "manager"]
        if value not in allowed_roles:
            raise ValueError(f"El rol debe ser uno de los siguientes: {', '.join(allowed_roles)}.")
        return value

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeRead(EmployeeBase):
    id: int

class EmployeeUpdate(SQLModel):
    name: Optional[str] = None
    role: Optional[str] = None