from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    buyer_name = Column(String(100), default="Cliente General")
    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("ProductModel")
    user = relationship("UserModel")
