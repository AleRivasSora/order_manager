from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.item import ItemCreate, ItemUpdate, ItemRead
from app.controllers.items_controller import ItemController
from app.database.database import get_db

router = APIRouter()


@router.post("/items/", response_model=ItemRead, status_code=201)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    try:
        item_controller = ItemController(db)
        return item_controller.create_item(item)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/items/{item_id}", response_model=ItemRead)
def get_item(item_id: int, db: Session = Depends(get_db)):
    try:
        item_controller = ItemController(db)
        return item_controller.get_item(item_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/items/{item_id}", response_model=ItemRead)
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    try:
        item_controller = ItemController(db)
        return item_controller.update_item(item_id, item)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/items/", response_model=list[ItemRead])
def list_items(db: Session = Depends(get_db)):
    try:
        item_controller = ItemController(db)
        return item_controller.get_all_items()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))