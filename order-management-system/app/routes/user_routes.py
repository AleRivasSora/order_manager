from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdate, UserRead
from app.controllers.user_controller import UserController
from app.database.database import get_db

router = APIRouter()

def get_user_controller(db: Session = Depends(get_db)) -> UserController:
    return UserController(db)

@router.post("/users/", response_model=UserRead, status_code=201)
def create_user(user: UserCreate, user_controller: UserController = Depends(get_user_controller)):
    """
    Create a new user.
    """
    return user_controller.create_user(user)

@router.get("/users/{user_id}", response_model=UserRead, responses={404: {"description": "User not found"}})
def get_user(user_id: int, user_controller: UserController = Depends(get_user_controller)):
    """
    Retrieve a user by ID.
    """
    return user_controller.get_user(user_id)

@router.put("/users/{user_id}", response_model=UserRead, responses={404: {"description": "User not found"}})
def update_user(user_id: int, user: UserUpdate, user_controller: UserController = Depends(get_user_controller)):
    """
    Update an existing user.
    """
    return user_controller.update_user(user_id, user)

@router.get("/users/", response_model=list[UserRead])
def list_users(skip: int = 0, limit: int = 10, user_controller: UserController = Depends(get_user_controller)):
    """
    List all users with pagination.
    """
    return user_controller.get_all_users(skip=skip, limit=limit)