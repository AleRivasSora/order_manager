from fastapi import HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserRead
from datetime import datetime
from passlib.hash import bcrypt

class UserController:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate) -> UserRead:
        try:
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
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error creating user: {str(e)}")

    def get_user(self, user_id: int) -> UserRead:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserRead.from_orm(user)

    def update_user(self, user_id: int, user_update: UserUpdate) -> UserRead:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        try:
            # Update only the fields provided in the UserUpdate schema
            update_data = user_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(user, key, value)
            self.db.commit()
            self.db.refresh(user)
            return UserRead.from_orm(user)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error updating user: {str(e)}")

    def get_all_users(self) -> List[UserRead]:
        try:
            users = self.db.query(User).all()
            return [UserRead.from_orm(user) for user in users]
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error retrieving users: {str(e)}")