from sqlalchemy import Column, Integer, String, DateTime
from app.database.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    orders = relationship("Order", back_populates="customer")  # Relación con Order