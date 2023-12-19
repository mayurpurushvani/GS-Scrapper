import sqlalchemy

from app.model.BaseModel import BaseModel


class Link(BaseModel):
    __tablename__ = "links"
    asin = sqlalchemy.Column(sqlalchemy.String(), nullable=False)
    link = sqlalchemy.Column(sqlalchemy.String(), nullable=False)
