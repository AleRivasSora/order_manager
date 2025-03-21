from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Nombre del producto
    description = Column(String, nullable=True)  # Descripción opcional
    price = Column(Float, nullable=False)  # Precio del producto
    stock = Column(Integer, default=0)  # Cantidad disponible en inventario
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)  # Relación con Order
    order = relationship("Order", back_populates="items")  # Relación inversa con Order