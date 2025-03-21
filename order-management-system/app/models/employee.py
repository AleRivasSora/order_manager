from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)  # Ejemplo: "waiter", "chef", "manager"
    created_at = Column(DateTime, default=datetime.utcnow)
    orders = relationship("Order", back_populates="employee")  # Relación con Order