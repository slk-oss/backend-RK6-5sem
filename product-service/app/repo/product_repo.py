from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product


class ProductRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Product]:
        stmt = select(Product).order_by(Product.product_id)
        return list(self.db.execute(stmt).scalars())

    def get_by_id(self, product_id: int) -> Product | None:
        return self.db.get(Product, product_id)