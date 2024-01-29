from app.db import db
from app.model.attribute import Attribute
from app.model.base_model import Base
from app.model.link import Link
from app.model.product import Product


class Database:
    @classmethod
    def init(cls):
        attribute = Attribute
        link = Link
        product = Product

        Base.metadata.create_all(bind=db.get_engine())
