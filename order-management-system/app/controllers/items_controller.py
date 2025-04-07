from fastapi import HTTPException
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate, ItemRead
from datetime import datetime


class ItemController:
    def __init__(self, db: Session):
        self.db = db

    def _get_item_by_id(self, item_id: int) -> Item:
        """
        Helper method to retrieve an item by ID.
        Raises an HTTPException if the item is not found.
        """
        item = self.db.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item

    def create_item(self, item: ItemCreate) -> ItemRead:
        """
        Creates a new item in the database.
        """
        try:
            # Check if an item with the same name already exists
            existing_item = self.db.query(Item).filter(Item.name == item.name).first()
            if existing_item:
                raise HTTPException(status_code=400, detail="Item with this name already exists")

            db_item = Item(**item.dict())
            self.db.add(db_item)
            self.db.commit()
            self.db.refresh(db_item)
            return ItemRead.from_orm(db_item)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Error creating item: Integrity constraint violated.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    def get_item(self, item_id: int) -> ItemRead:
        """
        Retrieves an item by ID.
        """
        item = self._get_item_by_id(item_id)
        return ItemRead.from_orm(item)

    def update_item(self, item_id: int, item_update: ItemUpdate) -> ItemRead:
        """
        Updates an existing item.
        """
        item = self._get_item_by_id(item_id)
        try:
            # Update only the fields provided in the ItemUpdate schema
            update_data = item_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(item, key, value)
            self.db.commit()
            self.db.refresh(item)
            return ItemRead.from_orm(item)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Error updating item: Integrity constraint violated.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    def get_all_items(self, skip: int = 0, limit: int = 10) -> List[ItemRead]:
        """
        Retrieves all items with pagination.
        """
        try:
            items = self.db.query(Item).offset(skip).limit(limit).all()
            return [ItemRead.from_orm(item) for item in items]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving items: {str(e)}")