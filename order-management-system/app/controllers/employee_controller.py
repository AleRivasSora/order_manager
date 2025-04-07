from fastapi import HTTPException
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeRead
from datetime import datetime


class EmployeeController:
    def __init__(self, db: Session):
        self.db = db

    def _get_employee_by_id(self, employee_id: int) -> Employee:
        """
        Helper method to retrieve an employee by ID.
        Raises an HTTPException if the employee is not found.
        """
        employee = self.db.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        return employee

    def create_employee(self, employee: EmployeeCreate) -> EmployeeRead:
        """
        Creates a new employee in the database.
        """
        try:
            # Check if an employee with the same email already exists
            existing_employee = self.db.query(Employee).filter(Employee.email == employee.email).first()
            if existing_employee:
                raise HTTPException(status_code=400, detail="Employee with this email already exists")

            db_employee = Employee(**employee.dict())
            self.db.add(db_employee)
            self.db.commit()
            self.db.refresh(db_employee)
            return EmployeeRead.from_orm(db_employee)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Error creating employee: Integrity constraint violated.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    def get_employee(self, employee_id: int) -> EmployeeRead:
        """
        Retrieves an employee by ID.
        """
        employee = self._get_employee_by_id(employee_id)
        return EmployeeRead.from_orm(employee)

    def update_employee(self, employee_id: int, employee_update: EmployeeUpdate) -> EmployeeRead:
        """
        Updates an existing employee.
        """
        employee = self._get_employee_by_id(employee_id)
        try:
            # Update only the fields provided in the EmployeeUpdate schema
            update_data = employee_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(employee, key, value)
            self.db.commit()
            self.db.refresh(employee)
            return EmployeeRead.from_orm(employee)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Error updating employee: Integrity constraint violated.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    def get_all_employees(self, skip: int = 0, limit: int = 10) -> List[EmployeeRead]:
        """
        Retrieves all employees with pagination.
        """
        try:
            employees = self.db.query(Employee).offset(skip).limit(limit).all()
            return [EmployeeRead.from_orm(employee) for employee in employees]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving employees: {str(e)}")