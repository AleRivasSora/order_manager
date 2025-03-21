from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdate, UserRead
from app.controllers.user_controller import UserController
from app.database.database import get_db

router = APIRouter()


@router.post("/users/", response_model=UserRead, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    try:
        user_controller = UserController(db)
        return user_controller.create_user(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a user by ID.
    """
    try:
        user_controller = UserController(db)
        return user_controller.get_user(user_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """
    Update an existing user.
    """
    try:
        user_controller = UserController(db)
        return user_controller.update_user(user_id, user)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/users/", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db)):
    """
    List all users.
    """
    try:
        user_controller = UserController(db)
        return user_controller.get_all_users()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))