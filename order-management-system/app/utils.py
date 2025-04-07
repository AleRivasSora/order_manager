from sqlalchemy.orm import Session
from fastapi import HTTPException

def validate_unique_field(db: Session, model, field: str, value: str, error_message: str):
    """
    Validates that a given field in a model is unique.
    Raises an HTTPException with status code 400 if the value already exists.
    """
    existing_record = db.query(model).filter(getattr(model, field) == value).first()
    if existing_record:
        raise HTTPException(status_code=400, detail=error_message)