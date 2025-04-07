from fastapi import HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserRead
from datetime import datetime
from passlib.hash import bcrypt
from app.utils import validate_unique_field


class UserController:
    def __init__(self, db: Session):
        self.db = db

    def _get_user_by_id(self, user_id: int) -> User:
        """
        Helper method to retrieve a user by ID.
        Raises an HTTPException if the user is not found.
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def create_user(self, user: UserCreate) -> UserRead:
        """
        Creates a new user in the database.
        """
        try:
            
            validate_unique_field(
            db=self.db,
            model=User,
            field="email",
            value=user.email,
            error_message="Email already in use"
        )

            hashed_password = bcrypt.hash(user.password)
            db_user = User(
                username=user.username,
                email=user.email,
                hashed_password=hashed_password,
                created_at=datetime.now()
            )
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return UserRead.from_orm(db_user)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="User with this email or username already exists.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    def get_user(self, user_id: int) -> UserRead:
        """
        Retrieves a user by ID.
        """
        user = self._get_user_by_id(user_id)
        return UserRead.from_orm(user)

    def update_user(self, user_id: int, user_update: UserUpdate) -> UserRead:
        """
        Updates an existing user.
        """
        user = self._get_user_by_id(user_id)
        try:
            # Update only the fields provided in the UserUpdate schema
            update_data = user_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(user, key, value)
            self.db.commit()
            self.db.refresh(user)
            return UserRead.from_orm(user)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Error updating user: Integrity constraint violated.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    def get_all_users(self, skip: int = 0, limit: int = 10) -> List[UserRead]:
        """
        Retrieves all users with pagination.
        """
        try:
            users = self.db.query(User).offset(skip).limit(limit).all()
            return [UserRead.from_orm(user) for user in users]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving users: {str(e)}")
        
    