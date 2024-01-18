from datetime import datetime, timezone

import sqlalchemy

from app.model.base_model import BaseModel


class Product(BaseModel):
    __tablename__ = "products"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(), nullable=False)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), nullable=True)
