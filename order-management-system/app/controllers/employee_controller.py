from fastapi import HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeRead
from datetime import datetime

class EmployeeController:
    def __init__(self, db: Session):
        self.db = db

    def create_employee(self, employee: EmployeeCreate) -> EmployeeRead:
        try:
            # Convert EmployeeCreate schema to Employee model
            db_employee = Employee(**employee.dict())
            self.db.add(db_employee)
            self.db.commit()
            self.db.refresh(db_employee)
            return EmployeeRead.from_orm(db_employee)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error creating employee: {str(e)}")

    def get_employee(self, employee_id: int) -> EmployeeRead:
        employee = self.db.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        return EmployeeRead.from_orm(employee)

    def update_employee(self, employee_id: int, employee_update: EmployeeUpdate) -> EmployeeRead:
        employee = self.db.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        try:
            # Update only the fields provided in the EmployeeUpdate schema
            update_data = employee_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(employee, key, value)
            self.db.commit()
            self.db.refresh(employee)
            return EmployeeRead.from_orm(employee)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error updating employee: {str(e)}")

    def get_all_employees(self) -> List[EmployeeRead]:
        try:
            employees = self.db.query(Employee).all()
            return [EmployeeRead.from_orm(employee) for employee in employees]
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error retrieving employees: {str(e)}")