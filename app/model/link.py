from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.model.base_model import BaseModel


class Link(BaseModel):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True, autoincrement=True)
    asin = Column(String(), nullable=False)
    link = Column(String(), nullable=False)
    is_scraped = Column(Boolean(), nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=True)
