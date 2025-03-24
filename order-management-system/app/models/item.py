from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.database.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)  
    description = Column(String(225), nullable=True)  
    price = Column(Float, nullable=False) 
    stock = Column(Integer, default=0)  
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)  
    order = relationship("Order", back_populates="items") 