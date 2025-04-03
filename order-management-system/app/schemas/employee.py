from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import field_validator

class EmployeeBase(SQLModel):
    name: str = Field(..., min_length=1, max_length=100, description="Employee's name")
    role: str = Field(..., description="Employee's role (e.g., 'chef', 'waiter')")

    @field_validator("role")
    def validate_role(cls, value):
        allowed_roles = ["chef", "waiter", "manager"]
        if value not in allowed_roles:
            raise ValueError(f"The role must be one of the following: {', '.join(allowed_roles)}.")
        return value

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeRead(EmployeeBase):
    id: int

class EmployeeUpdate(SQLModel):
    name: Optional[str] = None
    role: Optional[str] = None