from fastapi import HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate, ItemRead
from datetime import datetime

class ItemController:
    def __init__(self, db: Session):
        self.db = db

    def create_item(self, item: ItemCreate) -> ItemRead:
        try:
            # Convert ItemCreate schema to Item model
            db_item = Item(**item.dict())
            self.db.add(db_item)
            self.db.commit()
            self.db.refresh(db_item)
            return ItemRead.from_orm(db_item)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error creating item: {str(e)}")

    def get_item(self, item_id: int) -> ItemRead:
        item = self.db.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return ItemRead.from_orm(item)

    def update_item(self, item_id: int, item_update: ItemUpdate) -> ItemRead:
        item = self.db.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        try:
            # Update only the fields provided in the ItemUpdate schema
            update_data = item_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(item, key, value)
            self.db.commit()
            self.db.refresh(item)
            return ItemRead.from_orm(item)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error updating item: {str(e)}")

    def get_all_items(self) -> List[ItemRead]:
        try:
            items = self.db.query(Item).all()
            return [ItemRead.from_orm(item) for item in items]
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error retrieving items: {str(e)}")