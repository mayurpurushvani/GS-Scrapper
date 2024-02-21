from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Boolean, Text, DECIMAL, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.model.base_model import BaseModel


class Product(BaseModel):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, autoincrement=True)
    link_id = Column(Integer, ForeignKey("link.id"), unique=True, nullable=False)
    link = relationship("Link", uselist=False, single_parent=True, backref='product')
    sku = Column(String(255), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    published = Column(Boolean, default=False)
    visibility_in_catalog = Column(String(255), default='visible')
    short_description = Column(Text)
    description = Column(Text)
    in_stock = Column(Boolean, default=True)
    weight = Column(DECIMAL(10, 2), default=None)
    length = Column(DECIMAL(10, 2), default=None)
    width = Column(DECIMAL(10, 2), default=None)
    height = Column(DECIMAL(10, 2), default=None)
    allow_customer_reviews = Column(Boolean, default=True)
    sale_price = Column(DECIMAL(10, 2), nullable=False)
    regular_price = Column(DECIMAL(10, 2), nullable=False)
    categories = Column(String(255), default=None)
    tags = Column(String(255), default=None)
    images = Column(Text, default=None)
    external_url = Column(String(255), default=None)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=True)
