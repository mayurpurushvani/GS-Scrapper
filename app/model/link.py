from datetime import datetime, timezone

import sqlalchemy

from app.model.base_model import BaseModel


class Link(BaseModel):
    __tablename__ = "links"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    asin = sqlalchemy.Column(sqlalchemy.String(), nullable=False)
    link = sqlalchemy.Column(sqlalchemy.String(), nullable=False)
    is_scraped = sqlalchemy.Column(sqlalchemy.Boolean(), nullable=False, default=False)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), nullable=True)
