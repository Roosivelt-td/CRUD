from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from datetime import datetime
from app.database import Base
from pydantic import BaseModel
from typing import Optional

# --- MODEL (ORM) ---
class ItemModel(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# --- SCHEMAS (Data validation for Controller/Model interaction) ---
class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class ItemResponse(ItemBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
