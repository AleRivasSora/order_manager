from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.order import OrderCreate, OrderUpdate, OrderRead
from app.controllers.order_controller import OrderController
from app.database.database import get_db

router = APIRouter()

def get_order_controller(db: Session = Depends(get_db)) -> OrderController:
    return OrderController(db)

@router.post("/orders/", response_model=OrderRead, status_code=201)
def create_order(order: OrderCreate, order_controller: OrderController = Depends(get_order_controller)):
    """
    Create a new order.
    """
    return order_controller.create_order(order)

@router.get("/orders/{order_id}", response_model=OrderRead, responses={404: {"description": "Order not found"}})
def get_order(order_id: int, order_controller: OrderController = Depends(get_order_controller)):
    """
    Retrieve an order by ID.
    """
    return order_controller.get_order(order_id)

@router.put("/orders/{order_id}", response_model=OrderRead, responses={404: {"description": "Order not found"}})
def update_order(order_id: int, order: OrderUpdate, order_controller: OrderController = Depends(get_order_controller)):
    """
    Update an existing order.
    """
    return order_controller.update_order(order_id, order)

@router.get("/orders/", response_model=list[OrderRead])
def list_orders(skip: int = 0, limit: int = 10, order_controller: OrderController = Depends(get_order_controller)):
    """
    List all orders with pagination.
    """
    return order_controller.get_all_orders(skip=skip, limit=limit)