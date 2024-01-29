from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.model.base_model import BaseModel


class Attribute(BaseModel):
    __tablename__ = "product_attribute"
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    product = relationship("Product", backref='attributes')
    attribute = Column(String(255), nullable=False)
    value = Column(Text)
