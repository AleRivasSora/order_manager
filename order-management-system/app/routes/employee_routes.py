from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeRead
from app.controllers.employee_controller import EmployeeController
from app.database.database import get_db

router = APIRouter()


@router.post("/employees/", response_model=EmployeeRead, status_code=201)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    """
    Create a new employee.
    """
    try:
        employee_controller = EmployeeController(db)
        return employee_controller.create_employee(employee)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/employees/{employee_id}", response_model=EmployeeRead)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    """
    Retrieve an employee by ID.
    """
    try:
        employee_controller = EmployeeController(db)
        return employee_controller.get_employee(employee_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/employees/{employee_id}", response_model=EmployeeRead)
def update_employee(employee_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db)):
    """
    Update an existing employee.
    """
    try:
        employee_controller = EmployeeController(db)
        return employee_controller.update_employee(employee_id, employee)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/employees/", response_model=list[EmployeeRead])
def list_employees(db: Session = Depends(get_db)):
    """
    List all employees.
    """
    try:
        employee_controller = EmployeeController(db)
        return employee_controller.get_all_employees()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))