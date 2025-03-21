from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.order import OrderCreate, OrderUpdate, OrderRead
from app.controllers.order_controller import OrderController
from app.database.database import SessionLocal, get_db

router = APIRouter()


@router.post("/orders/", response_model=OrderRead, status_code=201)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    try:
        order_controller = OrderController(db)
        return order_controller.create_order(order)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/orders/{order_id}", response_model=OrderRead)
def get_order(order_id: int, db: Session = Depends(get_db)):
    try:
        order_controller = OrderController(db)
        return order_controller.get_order(order_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/orders/{order_id}", response_model=OrderRead)
def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    try:
        order_controller = OrderController(db)
        return order_controller.update_order(order_id, order)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/orders/", response_model=list[OrderRead])
def list_orders(db: Session = Depends(get_db)):
    try:
        order_controller = OrderController(db)
        return order_controller.get_all_orders()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))