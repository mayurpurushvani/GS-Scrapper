import sqlalchemy

from app.model.BaseModel import BaseModel


class Product(BaseModel):
    __tablename__ = "products"
    name = sqlalchemy.Column(sqlalchemy.String(), nullable=False)
    link = sqlalchemy.relationship('Link')
