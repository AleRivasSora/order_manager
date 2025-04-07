from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.item import ItemCreate, ItemUpdate, ItemRead
from app.controllers.items_controller import ItemController
from app.database.database import get_db

router = APIRouter()

def get_item_controller(db: Session = Depends(get_db)) -> ItemController:
    return ItemController(db)

@router.post("/items/", response_model=ItemRead, status_code=201)
def create_item(item: ItemCreate, item_controller: ItemController = Depends(get_item_controller)):
    """
    Create a new item.
    """
    return item_controller.create_item(item)

@router.get("/items/{item_id}", response_model=ItemRead, responses={404: {"description": "Item not found"}})
def get_item(item_id: int, item_controller: ItemController = Depends(get_item_controller)):
    """
    Retrieve an item by ID.
    """
    return item_controller.get_item(item_id)

@router.put("/items/{item_id}", response_model=ItemRead, responses={404: {"description": "Item not found"}})
def update_item(item_id: int, item: ItemUpdate, item_controller: ItemController = Depends(get_item_controller)):
    """
    Update an existing item.
    """
    return item_controller.update_item(item_id, item)

@router.get("/items/", response_model=list[ItemRead])
def list_items(skip: int = 0, limit: int = 10, item_controller: ItemController = Depends(get_item_controller)):
    """
    List all items with pagination.
    """
    return item_controller.get_all_items(skip=skip, limit=limit)