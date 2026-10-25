from sqlalchemy import select

from app.models.product import Product
from app.database import db


class ProductRepo: 
    def get_all(self) -> list[Product]:
        stmt = select(Product).order_by(Product.product_id) 
        return list(db.session.execute(stmt).scalars().all())

    def get_by_id(self, product_id: int) -> Product | None:
        return db.session.get(Product, product_id) 
