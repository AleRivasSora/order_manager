from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeRead
from app.controllers.employee_controller import EmployeeController
from app.database.database import get_db

router = APIRouter()

def get_employee_controller(db: Session = Depends(get_db)) -> EmployeeController:
    return EmployeeController(db)

@router.post("/employees/", response_model=EmployeeRead, status_code=201)
def create_employee(employee: EmployeeCreate, employee_controller: EmployeeController = Depends(get_employee_controller)):
    """
    Create a new employee.
    """
    return employee_controller.create_employee(employee)

@router.get("/employees/{employee_id}", response_model=EmployeeRead, responses={404: {"description": "Employee not found"}})
def get_employee(employee_id: int, employee_controller: EmployeeController = Depends(get_employee_controller)):
    """
    Retrieve an employee by ID.
    """
    return employee_controller.get_employee(employee_id)

@router.put("/employees/{employee_id}", response_model=EmployeeRead, responses={404: {"description": "Employee not found"}})
def update_employee(employee_id: int, employee: EmployeeUpdate, employee_controller: EmployeeController = Depends(get_employee_controller)):
    """
    Update an existing employee.
    """
    return employee_controller.update_employee(employee_id, employee)

@router.get("/employees/", response_model=list[EmployeeRead])
def list_employees(skip: int = 0, limit: int = 10, employee_controller: EmployeeController = Depends(get_employee_controller)):
    """
    List all employees with pagination.
    """
    return employee_controller.get_all_employees(skip=skip, limit=limit)