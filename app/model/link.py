from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.model.base_model import BaseModel


class Link(BaseModel):
    __tablename__ = "link"
    id = Column(Integer, primary_key=True, autoincrement=True)
    asin = Column(String(255), nullable=False)
    link = Column(String(255), nullable=False)
    is_scraped = Column(Boolean(), nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=True)
