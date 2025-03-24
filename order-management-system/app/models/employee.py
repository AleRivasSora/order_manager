from sqlalchemy import Column, Integer, String, DateTime
from app.database.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False) 
    role = Column(String(50), nullable=False)  
    created_at = Column(DateTime, default=datetime.now)
    orders = relationship("Order", back_populates="employee")  